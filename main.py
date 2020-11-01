from Extracao import extracao
from Transform import feature_engineering


def main():
    json = extracao()
    df = feature_engineering(json)
    print(df)

if __name__ == "__main__":
    main()
