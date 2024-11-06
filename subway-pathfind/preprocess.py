import pandas as pd

df = pd.read_csv("subway-pathfind/raw.csv", encoding="CP949")


def get_transfer(data):
    transfer = {}
    station = {}

    for i in range(len(data)):
        row = data.iloc[i]

        if row["역명"] == "응암": continue

        if row["역명"] in station.keys():
            if row["역명"] not in transfer.keys():
                transfer[row["역명"]] = [station[row["역명"]], row["호선"]]
            
            else:
                transfer[row["역명"]].append(row["호선"])

        else:
            station[row["역명"]] = row["호선"]


    transfer_bool = []

    for s in data["역명"]:
        transfer_bool.append(True if s in transfer else False)

    return transfer_bool


df["환승"] = get_transfer(df)
df.to_csv("subway-pathfind/data.csv", encoding="CP949")