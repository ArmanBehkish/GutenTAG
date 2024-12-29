import os
import shutil
import pandas as pd
import yaml


class MultiDimDataset:
    """
    Generates a multi-dimensional synthetic dataset using GutenTAG.
    Single Timeseries/Labels are produced serially, Then aggregated into one data and one label file.
    - instructions on the total number of series to produce and the cofig file associated with each are in the instructions.yaml file.
    - configs for each category of timeseries are in the configs folder.
    - outputs are generated in the outputs folder.
    - data.csv and labels.csv in the output_dataset folder.
    """

    def __init__(self, seed: int, n_jobs: int):
        self.num_series: int
        self.seed = seed
        self.n_jobs = n_jobs
        self.series_count = 0
        self.instructions: object
        self.output_series_file: str
        self.output_labels_file: str
        self.series_df: pd.DataFrame = pd.DataFrame()
        self.labels_df: pd.DataFrame = pd.DataFrame()
        self.path = "./Aggregate_Labels"
        self.config_path = "./configs"
        self.output_path = "./outputs"
        self.final_output_path = "./output_dataset"
        self.instructions_file = "./instructions.yaml"

    def read_instructions(self):
        """
        Reads instructions config file.
        """
        try:
            with open(
                os.path.join(os.getcwd(), self.path, self.instructions_file),
                "r",
                encoding="utf-8",
            ) as file:
                self.instructions = yaml.safe_load(file)
                self.num_series = self.instructions["num_series"]
                self.output_series_file = self.instructions["output_series_file"]
                self.output_labels_file = self.instructions["output_labels_file"]

        except FileNotFoundError:
            print("Instructions file not found")
            raise

    def clean_old_file(self):
        """
        Cleans the old files in the output_dataset folder.
        """
        final_output_path = os.path.join(os.getcwd(), self.path, self.final_output_path)
        output_path = os.path.join(os.getcwd(), self.path, self.output_path)

        # Clean output directories
        for path in [output_path, final_output_path]:
            if os.path.exists(path):
                for file in os.listdir(path):
                    file_path = os.path.join(path, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)

    def generate(self):
        """
        Reads the config files for each group.
        """
        # clean instructions file
        self.instructions = {
            k: v for k, v in self.instructions.items() if k.startswith("group_")
        }

        num_series_created = 0
        # iterate over each group
        for group, entries in self.instructions.items():
            # Convert list of dicts to a single dict
            entries = {
                list(entry.keys())[0]: list(entry.values())[0] for entry in entries
            }
            num_series_in_group = entries["number_of_series"]
            config_file = entries["config_file"]
            # read config file for the group
            with open(
                os.path.join(os.getcwd(), self.path, self.config_path, config_file),
                "r",
                encoding="utf-8",
            ) as f:
                config = yaml.safe_load(f)
                group_name = config["timeseries"][0]["name"]

            # print group info
            print(
                f"group: {group}, num_series_in_group: {num_series_in_group}, config_file: {config_file}, group_name: {group_name}\n\n"
            )

            # generating series
            num_to_create = self.num_series - num_series_created
            if num_to_create >= num_series_in_group:
                # generate all series in the group
                for i in range(num_series_in_group):
                    self.add_one_ts(config_file, group_name, i)
                num_series_created += num_series_in_group
            else:
                for i in range(num_to_create):
                    # remaining series to create is less than the number of series in the group
                    self.add_one_ts(config_file, group_name, i)
                num_series_created += num_to_create

    def add_one_ts(self, config_file, group_name, i):
        """
        Generates One timeserie. add the data and labels the the corresponding dataset files.

        """
        self.series_count += 1
        config_file_path = os.path.join(
            os.getcwd(), self.path, self.config_path, config_file
        )
        output_file_path = os.path.join(
            os.getcwd(), self.path, self.output_path, f"out_{self.series_count}"
        )
        final_output_path = os.path.join(os.getcwd(), self.path, self.final_output_path)

        os.system(
            f"python -m gutenTAG --config-yaml {config_file_path} --output-dir {output_file_path} --n-jobs {self.n_jobs} --seed {self.seed}{i}"
        )

        file_path = f"{output_file_path}/" + f"{group_name}/test.csv"
        # read the generated file in outputs/out_i/group_name/test.csv
        df = pd.read_csv(file_path).set_index("timestamp")
        # add the data to the series_df
        self.series_df = pd.concat([self.series_df, df["value-0"]], axis=1)
        self.series_df.columns.values[-1] = f"s{self.series_count}"

        # add the label to the labels_df
        self.labels_df = pd.concat([self.labels_df, df["is_anomaly"]], axis=1)
        self.labels_df.columns.values[-1] = f"l{self.series_count}"

        # writing to output files
        pd.DataFrame.to_csv(
            self.series_df, f"{final_output_path}/{self.output_series_file}"
        )
        pd.DataFrame.to_csv(
            self.labels_df, f"{final_output_path}/{self.output_labels_file}"
        )


if __name__ == "__main__":

    ds_obj = MultiDimDataset(seed=42, n_jobs=5)
    ds_obj.read_instructions()
    ds_obj.clean_old_file()
    ds_obj.generate()
