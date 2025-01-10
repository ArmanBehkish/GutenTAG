<div align="center">
    <img width="400px" src="https://github.com/TimeEval/gutentag/raw/main/logo_transparent.png" alt="TimeEval logo"/>
</div>

This Repository is forked from [TimeEval/gutentag](https://github.com/TimeEval/gutentag). A simple script is added to generate a multi-dimensional dataset with labels. It generates time series and labels one by one using config files provided and then combines all the time series in a data.csv file and all the labels in a labels.csv file. This is due to a use case in multi-dimensional time series anomaly detection where the algorithms usually require a dataset with a separate labels file.




## Usage

1. Install GutenTAG from [PyPI](https://pypi.org/project/timeeval-gutenTAG/):

   ```sh
   pip install timeeval-gutenTAG
   ```

   
2. Edit the instructions file [`instructions.yaml`](./Aggregate_Labels/instructions.yaml) to define groups of time series and the config file for each group. Also specify the total number of series to generate and the number from each group.

   ```yaml
   num_series: 9
    output_series_file: "data.csv"
    output_labels_file: "labels.csv"
    group_1:
      - number_of_series: 2
      - config_file: "config_1.yaml"
    group_2:
      - number_of_series: 2
      - config_file: "config_2.yaml"
    group_3:
      - number_of_series: 2
      - config_file: "config_3.yaml"
    group_4:
      - number_of_series: 3
      - config_file: "config_4.yaml"
   ```
  

3. Put the config files for each group in the [`configs`](./Aggregate_Labels/configs) folder.

4. Go to Aggregate_Labels directory and Run the script [`aggregate_labels.py`](./Aggregate_Labels/aggregate_labels.py) folder.

5. The output dataset will be in the [`output_dataset`](./Aggregate_Labels/output_dataset) folder, named `data.csv` and `labels.csv`.




