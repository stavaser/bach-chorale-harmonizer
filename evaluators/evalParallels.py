from music21 import *


def eval_parallel_octaves(chorale):
    total_intervals = 0
    parallel_octaves_count = 0

    offsetInfo = [get_offset_array(chorale.parts[0]), get_offset_array(chorale.parts[1]), get_offset_array(chorale.parts[2]), get_offset_array(chorale.parts[3])]

    partNames = ["soprano", "alto", "tenor", "bass"]

    for partNumber1 in range(4):
        for partNumber2 in range(partNumber1 + 1, 4):
            offsets1, offsetDict1 = offsetInfo[partNumber1]
            offsets2, offsetDict2 = offsetInfo[partNumber2]
            for offset in offsets1[:-1]:
                if offset in offsets2 and offset != offsets2[-1]:
                    total_intervals += 1
                    int1 = interval.Interval(offsetDict1[offset], offsetDict2[offset])
                    int2 = interval.Interval(offsetDict1[offsets1[offsets1.index(offset)+1]], offsetDict2[offsets2[offsets2.index(offset)+1]])
                    if int1 == int2 == interval.Interval('P8') or int1 == int2 == interval.Interval("P-8"):
                        parallel_octaves_count += 1

    score = 100 - (parallel_octaves_count / total_intervals * 100) if total_intervals > 0 else 100
    return score

def eval_parallel_fifths(chorale):
    total_intervals = 0
    parallel_fifths_count = 0

    offsetInfo = [get_offset_array(chorale.parts[0]), get_offset_array(chorale.parts[1]), get_offset_array(chorale.parts[2]), get_offset_array(chorale.parts[3])]
    partNames = ["soprano", "alto", "tenor", "bass"]

    for partNumber1 in range(4):
        for partNumber2 in range(partNumber1 + 1, 4):
            offsets1, offsetDict1 = offsetInfo[partNumber1]
            offsets2, offsetDict2 = offsetInfo[partNumber2]
            for offset in offsets1[:-1]:
                if offset in offsets2 and offset != offsets2[-1]:
                    total_intervals += 1
                    int1 = interval.Interval(offsetDict1[offset], offsetDict2[offset])
                    int2 = interval.Interval(offsetDict1[offsets1[offsets1.index(offset)+1]], offsetDict2[offsets2[offsets2.index(offset)+1]])
                    if int1 == int2 == interval.Interval('P5') or int1 == int2 == interval.Interval('P-5'):
                        parallel_fifths_count += 1

    score = 100 - (parallel_fifths_count / total_intervals * 100) if total_intervals > 0 else 100
    return score

    
def eval_parallel_unisons(chorale):
    total_intervals = 0
    parallel_unisons_count = 0

    offsetInfo = [get_offset_array(chorale.parts[0]), get_offset_array(chorale.parts[1]), get_offset_array(chorale.parts[2]), get_offset_array(chorale.parts[3])]
    partNames = ["soprano", "alto", "tenor", "bass"]

    for partNumber1 in range(4):
        for partNumber2 in range(partNumber1 + 1, 4):
            offsets1, offsetDict1 = offsetInfo[partNumber1]
            offsets2, offsetDict2 = offsetInfo[partNumber2]
            for offset in offsets1[:-1]:
                if offset in offsets2 and offset != offsets2[-1]:
                    total_intervals += 1
                    int1 = interval.Interval(offsetDict1[offset], offsetDict2[offset])
                    int2 = interval.Interval(offsetDict1[offsets1[offsets1.index(offset)+1]], offsetDict2[offsets2[offsets2.index(offset)+1]])
                    if int1 == int2 == interval.Interval('P1'):
                        parallel_unisons_count += 1

    score = 100 - (parallel_unisons_count / total_intervals * 100) if total_intervals > 0 else 100
    return score

def get_offset_array(part):
    offsetDict = {}
    offsets = []
    measureNumber = -1
    for elementA in range(len(part)):
        if isinstance(part[elementA], stream.Measure):
            measureNumber = measureNumber + 1
            for elementB in range(len(part[elementA])):
                if isinstance(part[elementA][elementB], note.Note):
                    offsetDict[round(measureNumber+part[elementA][elementB].beat*(0.1),4)] = part[elementA][elementB]
                    offsets.append(round(measureNumber+part[elementA][elementB].beat*(0.1),4))
    return [offsets, offsetDict]
        