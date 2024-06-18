from summarization.topic_aware_summarization.topic_aware_summarization import get_similarity_matrix


def run(text):
    dict_topic_sentences = get_similarity_matrix(text)
    print(dict_topic_sentences)

run('This American Psychologist open-access article lays out—for the first time—journal article reporting standards for qualitative research in psychology (Levitt, H.M., et al., Vol. 73, No. 1). The voluntary guidelines are designed to help authors communicate their work clearly, accurately and transparently. Developed by a working group of the APA Publications and Communications Board, the new standards describe what should be included in a qualitative research report, as well as in qualitative meta-analyses and mixed-methods research reports. They cover a range of qualitative traditions, methods and reporting styles. The article presents these standards and their rationale, details the ways they differ from quantitative research reporting standards and describes how they can be used by authors as well as by reviewers and editors.')
