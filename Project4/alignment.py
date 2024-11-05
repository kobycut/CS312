def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap='-'
) -> tuple[float, str | None, str | None]:
    """
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap: the character to use to represent gaps in the alignment strings
        :return: alignment cost, alignment 1, alignment 2
    """
    use_banded = False
    if banded_width != -1:
        use_banded = True
    if use_banded:
        banded_width = banded_width * 2 + 1

    matrix = [[0 for x in range(len(seq2) + 1)] for y in range(len(seq1) + 1)]

    if use_banded:
        pass

    else:
        for i in range(len(seq1) + 1):
            matrix[i][0] = i * indel_penalty
        for j in range(len(seq2) + 1):
            matrix[0][j] = j * indel_penalty

    if use_banded:
        pass


    else:
        for i in range(1, len(seq1) + 1):
            for j in range(1, len(seq2) + 1):
                if seq1[i - 1] == seq2[j - 1]:
                    diag = matrix[i - 1][j - 1] + match_award
                else:
                    diag = matrix[i - 1][j - 1] + sub_penalty
                up = matrix[i][j - 1] + indel_penalty
                left = matrix[i - 1][j] + indel_penalty

                matrix[i][j] = min(diag, up, left)

    optimal_cost = matrix[len(seq1)][len(seq2)]

    # back track
    align1 = ""
    align2 = ""
    x = len(seq1)
    y = len(seq2)
    while x > 0 or y > 0:
        if x > 0 and y > 0 and seq1[x - 1] == seq2[y - 1] and matrix[x][y] == matrix[x - 1][y - 1] + match_award:
            align1 = seq1[x - 1] + align1
            align2 = seq2[y - 1] + align2
            x -= 1
            y -= 1
        elif x > 0 and y > 0 and matrix[x][y] == matrix[x - 1][y - 1] + sub_penalty:
            align1 = seq1[x - 1] + align1
            align2 = seq2[y - 1] + align2
            x -= 1
            y -= 1

        elif x > 0 and matrix[x][y] == matrix[x - 1][y] + indel_penalty:
            align1 = seq1[x - 1] + align1
            align2 = gap + align2
            x -= 1
        elif y > 0 and matrix[x][y] == matrix[x][y - 1] + indel_penalty:
            align1 = gap + align1
            align2 = seq2[y - 1] + align2
            y -= 1

    return optimal_cost, align1, align2


# ATCTGG ATGGG
print(align('atcgt', 'agtcga', -3, 5, 1, -1, '-'))
# print(align('ATCTGG', 'ATGGG', -3, 5, 1, -1, '-'))
