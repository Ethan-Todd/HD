TARGET = {
    "ticker": "HD",
    "name": "The Home Depot",
    "price": 319.77,
    "diluted_eps": 14.23,
}

PEERS = [
    {
        "ticker": "LOW",
        "name": "Lowe's",
        "price": 200.05,
        "diluted_eps": 11.85,
    },
    {
        "ticker": "TSCO",
        "name": "Tractor Supply",
        "price": 34.71,
        "diluted_eps": 2.06,
    },
]


def is_positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def median(values):
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


target_ticker = str(TARGET.get("ticker", "")).strip().upper()
unique_peers = []
seen_tickers = set()

for peer in PEERS:
    ticker = str(peer.get("ticker", "")).strip().upper()
    if not ticker or ticker == target_ticker or ticker in seen_tickers:
        continue
    seen_tickers.add(ticker)
    unique_peers.append(peer)

valid_peers = []

print("Peer P/E calculations")
for peer in unique_peers:
    ticker = str(peer.get("ticker", "")).strip().upper()
    price = peer.get("price")
    diluted_eps = peer.get("diluted_eps")

    if not is_positive_number(price) or not is_positive_number(diluted_eps):
        print(f"{ticker} P/E: not meaningful")
        continue

    pe_ratio = price / diluted_eps
    valid_peers.append({"ticker": ticker, "pe_ratio": pe_ratio})
    print(f"{ticker} P/E: {pe_ratio:.6f}x")

target_eps = TARGET.get("diluted_eps")

print("\nTarget implied prices")
if not is_positive_number(target_eps):
    print("Target diluted EPS: not meaningful")
elif not valid_peers:
    print("No usable peers")
else:
    peer_multiples = [peer["pe_ratio"] for peer in valid_peers]
    minimum_pe = min(peer_multiples)
    median_pe = median(peer_multiples)
    maximum_pe = max(peer_multiples)
    full_peer_estimate = median_pe * target_eps

    print(f"Minimum peer P/E: {minimum_pe:.6f}x")
    print(f"Median peer P/E: {median_pe:.6f}x")
    print(f"Maximum peer P/E: {maximum_pe:.6f}x")

    if len(valid_peers) == 1:
        print(f"Reference estimate: ${full_peer_estimate:.2f}")
        print("Peer-implied range: no range with one valid peer")
    else:
        print(f"Minimum implied price: ${minimum_pe * target_eps:.2f}")
        print(f"Median implied price: ${full_peer_estimate:.2f}")
        print(f"Maximum implied price: ${maximum_pe * target_eps:.2f}")
        print(
            f"Peer-implied range: ${minimum_pe * target_eps:.2f}"
            f"-${maximum_pe * target_eps:.2f}"
        )

    print("\nPeer-removal tests")
    for removed_peer in valid_peers:
        remaining_multiples = [
            peer["pe_ratio"]
            for peer in valid_peers
            if peer["ticker"] != removed_peer["ticker"]
        ]

        if not remaining_multiples:
            print(f"Remove {removed_peer['ticker']}: no estimate")
            continue

        remaining_estimate = median(remaining_multiples) * target_eps
        dollar_change = remaining_estimate - full_peer_estimate
        change_text = f"${abs(dollar_change):.2f}"
        if dollar_change > 0:
            change_text = "+" + change_text
        elif dollar_change < 0:
            change_text = "-" + change_text
        print(
            f"Remove {removed_peer['ticker']}: "
            f"${remaining_estimate:.2f}; change {change_text}"
        )

print("\nThis classroom exercise is not financial advice.")
