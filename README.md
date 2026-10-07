# vidhance-extendview

Experiments in dehazing and infrared/visible fusion.

```
fusion/            infrared + visible fusion pipelines
  data/            inputs
  out/             outputs
dehazing/          dehazing pipelines
  data/
  out/
```

## Inputs

`<category>/data/<source>/` holds one scene: `rgb/` + `ir/` image sequences, frame-aligned with the same
filenames (`visible.mp4` + `thermal.mp4` also works). `data/` is not in git, except for the sample below.

`fusion/data/car_008/` is included: the first 5 s (150 frames, 1920x1080) of VTUAV sequence `car_008`.
`rgb.txt` / `ir.txt` are the dataset's tracking ground truth, one `x y w h` box per 10th frame, annotated
separately for each modality.

## Outputs

`<category>/out/<method>_<source>.mp4`

## Running

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Open a notebook with the `.venv` kernel, set `SOURCE` to a folder name in `data/`, run all cells.
