def minMaxAvg(testList=[1,2,3,4,5]):
    """
    최소최대값을 뺀 평균
    parameter: testList = 리스트
    return: 리스트내 값에서 최소 최대값을 뺸 평균을 반환한다.
    """
    # testList = [1,5,7,2,6,8,2,5,11]
    minValue = min(testList)
    maxValue = max(testList)
    print("최대값{} 최소값{}".format(minValue, maxValue) )

    testList.remove(minValue)
    testList.remove(maxValue)

    average = 0
    if len( testList ) != 0:
        average = sum(testList)/len( testList )
    else:
        pass

    return average