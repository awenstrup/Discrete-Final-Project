# Discrete-Final-Project

## Setup

To set up this demo, follow these steps:

1. Clone this repo
2. Install this repo with `pip install -e .`
3. Get coding!

## Usage

To use this tool, look at the code or refer to the demo below

```python
from hamming import main
a = main.encode("Hello world")  # encode a string as an array of codewords
main.add_noise(a, 0.02)  # add noise to the data
print(main.decode(a))  # check if the decoding worked
