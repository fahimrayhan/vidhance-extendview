import cv2
import numpy as np
import pyiqa
import torch
from skimage.color import deltaE_ciede2000, rgb2lab
from skimage.metrics import structural_similarity

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


#with GT
def psnr(pred, gt):
    #10 * log10(255^2 / MSE). higher is better
    mse = np.mean((pred.astype(np.float64) - gt.astype(np.float64)) ** 2)
    return float("inf") if mse == 0 else 10 * np.log10(255.0 ** 2 / mse)


def ssim(pred, gt):
    #structural similarity, higher is better
    return structural_similarity(gt, pred, channel_axis=2, data_range=255)


def ciede2000(pred, gt):
    #mean CIEDE2000 color difference in CIELAB, lower is better
    return np.mean(deltaE_ciede2000(rgb2lab(gt[..., ::-1]), rgb2lab(pred[..., ::-1])))

LPIPS = pyiqa.create_metric("lpips", device=DEVICE)

def lpips(pred, gt):
    #learned perceptual image patch similarity,lower is better
    return LPIPS(to_tensor(pred), to_tensor(gt)).item()


#without GT
NIQE = pyiqa.create_metric("niqe", device=DEVICE)
BRISQUE = pyiqa.create_metric("brisque", device=DEVICE)


def to_tensor(img):
    """uint8 BGR (H, W, 3) -> float RGB tensor (1, 3, H, W) in [0, 1], as pyiqa expects."""
    return torch.from_numpy(img[..., ::-1].copy()).permute(2, 0, 1)[None].float().div(255).to(DEVICE)


def niqe(pred):
    #natural image quality evaluator, lower is better
    return NIQE(to_tensor(pred)).item()


def brisque(pred):
    #blind referenceless image spatial quality evaluator, lower is better
    return BRISQUE(to_tensor(pred)).item()


#with hazy input, Hautiere et al. (2008) simplified
def gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def visible_edges(g):
    #low thresholds, otherwise heavy haze gives no edges at all
    return cv2.Canny(g, 20, 60) > 0


def gradient(g):
    return np.hypot(cv2.Sobel(g, cv2.CV_64F, 1, 0), cv2.Sobel(g, cv2.CV_64F, 0, 1))


def new_edges(pred, hazy):
    #e, rate of new visible edges, higher is better
    n_r, n_o = visible_edges(gray(pred)).sum(), visible_edges(gray(hazy)).sum()
    return (n_r - n_o) / n_o


def gradient_ratio(pred, hazy):
    #r, geometric mean of gradient gain at visible edges, higher is better
    gp, gh = gray(pred), gray(hazy)
    edges = visible_edges(gp)
    ratio = (gradient(gp)[edges] + 1) / (gradient(gh)[edges] + 1)
    return np.exp(np.mean(np.log(ratio)))


def saturation(pred, hazy):
    #sigma, fraction of pixels newly turned pure black or white, lower is better
    sat = lambda g: (g == 0) | (g == 255)
    return np.mean(sat(gray(pred)) & ~sat(gray(hazy)))


FULL_REF = {"psnr": psnr, "ssim": ssim, "ciede2000": ciede2000, "lpips": lpips}
NO_REF = {"niqe": niqe, "brisque": brisque}
HAZY_REF = {"e": new_edges, "r": gradient_ratio, "sigma": saturation}