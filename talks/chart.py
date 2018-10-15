from io import BytesIO
import matplotlib.pyplot as plt


def generate_survey_score_chart(talk, format="png"):
    ss = talk.surveyscore
    keys = [int(x) for x in ss.distribution.keys()]
    values = list(ss.distribution.values())
    subtitle = "avg={:.2f} n={}".format(ss.average, ss.count)
    title = "{}\n{}".format(str(talk), subtitle)

    plt.clf()
    plt.title(title)
    plt.bar(keys, values)
    plt.xlabel('Score')
    plt.ylabel('Count')
    plt.grid(True, axis='y', alpha=0.4)

    io = BytesIO()
    plt.savefig(io, format=format)
    return io.getvalue()
