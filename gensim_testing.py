# import modules & set up logging
from __future__ import print_function

import gensim


def testing_gensim(sentences):

    # create the model
    model = gensim.models.Word2Vec(sentences, size=5,
                                   alpha=0.025,
                                   min_alpha=0.0001,
                                   sg=1,
                                   iter=500,
                                   window=1,
                                   cbow_mean=0,
                                   seed=12,
                                   min_count=0,
                                   negative=1,
                                   hs=1)

    # sort by name so the order will be right
    sorted_list = sorted(model.wv.index2word)

    # get the score of each node by compering it to all the other nodes
    score_list = [model.n_similarity(sorted_list, [x]) for x in sorted_list]

    # print the score of each node for debugging
    answer_list = [(x,model.n_similarity(sorted_list, [x])) for x in sorted_list]
    print(*answer_list, sep="\n")

    return score_list
