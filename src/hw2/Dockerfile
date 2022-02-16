FROM gqcg/latex
COPY . .

RUN apt-get update && apt-get install -y graphviz
RUN python3 -m pip install graphviz
RUN python3 -m pip install --upgrade --index-url https://test.pypi.org/simple/ plekhanov_hw1==0.0.8

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh
CMD conda --version
RUN conda install conda-forge::python-graphviz conda-forge::graphviz=2.46.1

CMD python3 to_latex.py
