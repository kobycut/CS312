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
    matrix = [[0 for x in range(len(seq1))] for y in range(len(seq2))]

    for i in range(len(seq1)):
        matrix[i][0] = i * indel_penalty
    for j in range(len(seq2)):
        matrix[0][j] = j * indel_penalty

    for i in range(1, len(seq1)):
        for j in range(1, len(seq2)):
            if seq1[i] == seq2[j]:
                diag = matrix[i-1][j-1] + match_award
            else:
                diag = matrix[i-1][j-1] + sub_penalty
            up = matrix[i][j-1] + indel_penalty
            left = matrix[i-1][j] + indel_penalty

            matrix[i][j] = min(diag, up, left)

    # return alignment cost, seq 1 aligned, seq 2 aligned

