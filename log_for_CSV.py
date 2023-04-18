import pandas as pd
import os
import datetime



class Log:
    def first_log(self, first_time):
        self.first_time = first_time

    def logging(
            self, situation: str, questionnaire: str
    ):
        self.situation = situation
        self.questionnaire = questionnaire

        filepath = f"C:\\Users\\maglab\\Desktop\\kimoto\\vscode_project\\zikken\\Concentration_estimation_experiment\\log_dir\\{self.first_time}.csv"
        columns = ["時間", "状態", "アンケート"]

        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y_%m_%d_%H.%M.%S')
        print(time)
        self.log_data = {
            "時間": [],
            "状態": [],
            "アンケート":[]
        }
        self.log_data["時間"].append(time)
        self.log_data["状態"].append(self.situation)
        self.log_data["アンケート"].append(self.questionnaire)

        if os.path.isfile(filepath):
            df1 = pd.read_csv(filepath, encoding="shift_jis")
            df2 = pd.DataFrame(self.log_data)
            df = pd.merge(df1, df2, how="outer")
            df.to_csv(
                filepath,
                encoding="shift_jis",
                index=False,
            )
        else:
            df = pd.DataFrame(self.log_data)
            df.to_csv(
                filepath,
                encoding="shift_jis",
                index=False,
                columns=columns
            )