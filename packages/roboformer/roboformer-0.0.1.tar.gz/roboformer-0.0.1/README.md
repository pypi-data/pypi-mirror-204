# Roboformer

Roboformer, the embodied toolformer.

## Getting Started

### Requirements

- Python 3.10 or above
- PyTorch 2.0 or above

### Installation

Install using Pip:

> **Warning**
> This method doens't work yet.

```bash
pip install roboformer
```

Install from source:

```bash
git clone git@github.com:codekansas/roboformer.git
cd roboformer && pip install -e '.[dev]'
```

## Training a model

Train a model for a given config:

```bash
roboformer train configs/roboformer.yaml
```
