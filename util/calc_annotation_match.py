import json
import sys

with open("annoyances.json") as file:
    annoyances = json.load(file)

classes = list(annoyances.keys())


def calc_annotation_match(true_annotation, pred_annotation):
    match = {}

    def annotation_len(annotation, class_):
        return sum([event['end'] - event['start'] if event['class'] == class_ else 0 for event in annotation])

    def annotation_overlap_len(annotation1, annotation2, class_):
        sum_ = 0
        for event1 in annotation1:
            for event2 in annotation2:
                if event1['class'] == class_ and event2['class'] == class_:
                    sum_ += max(0, min(event1['end'], event2['end']) - max(event1['start'], event2['start']))
        return sum_

    for class_ in classes:
        true_annotation_len = annotation_len(true_annotation, class_)
        pred_annotation_len = annotation_len(pred_annotation, class_)
        overlap_annotation_len = annotation_overlap_len(true_annotation, pred_annotation, class_)
        match[class_] = (true_annotation_len, pred_annotation_len, overlap_annotation_len)

    return match


if __name__ == '__main__':
    true_annotation_filepath = sys.argv[1]
    pred_annotation_filepath = sys.argv[2]


    def read_annotation(filepath):
        events = []
        with open(filepath) as file:
            for line in file:
                try:
                    split = line.split('\t')
                    event = {'start': float(split[0]), 'end': float(split[1]), 'class': split[2].rstrip()}
                    events.append(event)
                except:
                    pass  # skip line
        return events


    true_annotation = read_annotation(true_annotation_filepath)
    pred_annotation = read_annotation(pred_annotation_filepath)

    match = calc_annotation_match(true_annotation, pred_annotation)

    for class_, match_scores in match.items():
        recall = match_scores[2] / match_scores[0] if match_scores[0] else None
        precision = match_scores[2] / match_scores[1] if match_scores[1] else None
        accuracy = 1 - (match_scores[0] + match_scores[1] - 2 * match_scores[2]) / 60.0
        print(class_, match_scores, recall, precision, accuracy)
