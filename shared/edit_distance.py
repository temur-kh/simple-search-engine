def levinstein_distance(word_from: str, word_to: str) -> int:
    N, M = len(word_from), len(word_to)
    dp = [[0 for _ in range(M + 1)] for _ in range(N + 1)]
    for i in range(N + 1):
        dp[i][0] = i
    for i in range(M + 1):
        dp[0][i] = i
    for i in range(1, N + 1, 1):
        for j in range(1, M + 1, 1):
            dp[i][j] = min(dp[i - 1][j - 1] +
                           (1 if word_from[i - 1] != word_to[j - 1] else 0),
                           dp[i - 1][j] + 1, dp[i][j - 1] + 1)
    return dp[N][M]
