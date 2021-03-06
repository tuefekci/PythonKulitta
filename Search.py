import random
import sys
import QuotientSpaces
def nextSol(buckets, pre):
    code = None
    res = []
    codes = []
    # print(pre)
    if pre is None:
        codes = (['1'] * len(buckets))
    else:
        pre_codes = pre.split("-")
        carry = 1
        for i2 in range(len(pre_codes)):
            if  carry == 1 and int(pre_codes[i2]) <= len(buckets[i2]) - 1:
                codes.append(str(int(pre_codes[i2]) + 1))
                carry = 0
            elif carry == 1 and int(pre_codes[i2]) == len(buckets[i2]):
                codes.append(str(1))
            else:
                codes.append(pre_codes[i2])

    for i2 in range(len(buckets)):
        res.append(buckets[i2][int(codes[i2]) - 1])
    codes = "-".join(codes)
    return codes, res


def allSols(qspace, eqrel, bucket):
    targets = []
    for val in bucket:
        tar = QuotientSpaces.eqClass(qspace, eqrel, val)
        if len(tar) == 0:
            raise Exception('error','No class for'+str(val))
        targets.append(tar)
    return allSolsHelper(targets)

def allSolsHelper(buckets):
    num = 1
    for b in buckets:
        num *= len(b)
    pre = None
    res = []
    for iter in range(num):
        pre, cur  = nextSol(buckets, pre)
        res.append(cur)
    # print(res)
    return res

class Predicate: # f(a) # f(a, b)
    def __init__(self, fn, single=False):
        self.fn = fn
        self.single = single

    def is_single(self):
        return self.single

    def compare(self, a, b= None):
        if self.single is True:
            return self.fn(a)
        else:
            return self.fn(a,b)
    def compareAll(self, arr):
        if self.single is True:
            for i2 in arr:
                if self.fn(i2) is False:
                    return False
        else:
            for i2 in range(len(arr) - 1):
                if self.fn(arr[i2], arr[i2+1]) is False:
                    return False
        return True
def pairProg(qspace, eqrel, constraint, bucket):
    targets = []
    for val in bucket:
        tar = QuotientSpaces.eqClass(qspace, eqrel, val)
        if len(tar) == 0:
            raise Exception('error', 'No class for' + str(val))
        targets.append(tar)
    res = []
    pairProgHelper(targets, constraint, 0, [], res)
    return res

def pairProgHelper(buckets, constraint, ith, pre, res):
    if ith == len(buckets):
        res.append(pre)
        return
    for candidate in buckets[ith]:
        if len(pre) == 0 or constraint(pre[-1], candidate) is True:
            pairProgHelper(buckets, constraint, ith + 1, pre + [candidate], res)


# def pairProg(buckets, c):
#     cur = None
#     num = 1
#     for b in buckets:
#         num *= len(b)
#     res = []
#     next = None
#     for i in range(num):
#         next, arr = nextSol(buckets, cur)
#         cur = next
#         suc = c.compareAll(arr)
#         if suc is True:
#             res.append(arr)
#     if len(res) == 1:
#         print("No solutions that satisfy the consraints!")
#     else:
#         return res

class Fallback:
    def __init__(self, fn = None):
        self.fn = fn
    def gen(self, bucket, pre = None):
        if self.fn is None or pre is None:
            return random.choice(bucket)
        return self.fn(bucket, pre)
# def greedyProg(buckets, fallback, c):
#     sol = []
#     pre = None
#     for idx in range(len(buckets)):
#         # idx = 0 random choose
#         # choose candidates from pre, if null then use falback
#         if idx == 0:
#             pre = random.choice(buckets[0])
#             sol.append(pre)
#             continue
#         can = []
#         for val in buckets[idx]:
#             if c.is_single() is True:
#                 if c.compare(val) is True:
#                     can.append(val)
#             elif c.is_single() is False:
#                 if c.compare(val, pre) is True:
#                     can.append(val)
#         # print(pre, can)
#         if len(can):
#             pre = random.choice(can)
#         else:
#             pre = fallback.gen(buckets[idx], pre)
#         sol.append(pre)
#     return sol
def greedyProg(qspace, eqrel, constraint, fallback, bucket):
    sol = []
    pre = None
    for idx in range(len(bucket)):
        val = bucket[idx]
        tar = QuotientSpaces.eqClass(qspace, eqrel, val)
        can = []
        if idx != 0:
            for t in tar:
                if constraint(pre, t) is True:
                    can.append(t)
        else:
            can = tar
        if len(can) == 0:
            pre = fallback(tar, pre)
        else:
            pre = random.choice(can)
        sol.append(pre)
    return sol
def nearFall(bucket, pre):
    # abs(i - pre)
    minV = sys.maxint
    minAbs = sys.maxint
    for val in bucket:
        if abs(val - pre) < minAbs:
            minAbs = abs(val - pre)
            minV = val
    return minV

# # for testing:
# A = [1, 2]
# B = [3, 4]
# # C = [1,0, 5, 6]
# buckets = [A, B]
# # code, arr = nextSol(buckets, "0-0")
# # print(code)
# # print(arr)
# print("all solution:")
# print(allSols(buckets))
#
# def absSmaller2(a, b):
#     return abs(a - b) <= 2
# p = Predicate(absSmaller2, False)
# a = 10
# b = 6
# print(p.compare(a, b))
# res = pairProg(buckets, p)
# print(res)
#
# print("Test for nearFall:")
# print("closest to 1 is:")
# print(nearFall([12, 0, 5], 1))
#
# print("Test for greedy Prog")
# buckets = [[2, 4], [5, 4]]
# def absSmaller1(a, b):
#     return abs(a - b) <= 1
# fallback = Fallback(nearFall)
# p2 = Predicate(absSmaller2, False)
# print(greedyProg(buckets, fallback, p2))
