# coding=utf-8
# 快排：一次遍历需要O(N)时间，递归深度 O(logN)，总共需要 O(NlogN) 时间复杂度。
def test(li1, start, end):
    # 必须加判断条件：否则会造成递归栈溢出（思考为什么）
    if start >= end:
        return
    mid = start
    # i和j:队头和队尾指针，移动的是i 和 j，不是 start 和 end
    i = start
    j = end
    while i < j:
        # j：比 mid 的值小的元素下标
        while i < j and li1[j] >= li1[mid]:
            j -= 1
        print "j=", end
        print "mid=", mid
        # 交换 mid 和 j 的值
        if mid != j:
            tmp = li1[j]
            li1[j] = li1[mid]
            li1[mid] = tmp
            mid = j
        print li1
        while i < j and li1[i] <= li1[mid]:
            i += 1
        print "i=", i
        # 交换 i 和 mid 的值
        if i != mid:
            tmp = li1[i]
            li1[i] = li1[mid]
            li1[mid] = tmp
            mid = i
            # 打印此时的数组
        print li1

    print mid
    test(li1, start, mid - 1)
    test(li1, mid + 1, end)


a = [0, 1, 2, 5, 7, 3, 3, 4]
test(a, 0, len(a) - 1)
print a
