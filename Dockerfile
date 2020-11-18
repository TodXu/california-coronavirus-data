FROM python:3

# Create the environment:
COPY requirements.txt .
RUN py -m pip install -r requirements.txt
ADD script.py /
ADD cdph-race-ethnicity.csv /
ADD latimes-state-totals.csv /
CMD ["bokeh", "serve", "--show", "script.py"]