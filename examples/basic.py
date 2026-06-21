from timeglance import forecast


def main() -> None:
    items = forecast(range(1000), sample_size=25, update_every=100)

    for _ in items:
        pass

    print(items.latest)


if __name__ == "__main__":
    main()
