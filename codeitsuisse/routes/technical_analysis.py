import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
import numpy, scipy.optimize
import numpy as np
# import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)

@app.route('/technical-analysis', methods=['POST'])
def technical_analysis():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    result = []
    for i,ar in enumerate(data):
        candidates = []
        for _ in range(10):
            try:
                candidates.append(optimise_case(ar, casenum = i))
            except Exception as e: 
                print(e)
        if len(candidates) == 0:
            result.append([100,1099])
        else:
            # print(candidates, "candidates")
            indice = np.argmin([c["loss"] for c in candidates])
            result.append(candidates[indice]["ans"])
            print(candidates[indice]["loss"])

    return jsonify(result)


def fit_sin_base(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = numpy.array(tt)
    yy_ = [yyy for yyy in yy]
    yy = numpy.array(yy_)

    yy = numpy.array(yy)
    # if np.random.randn() > 0.5:
    #     yy += np.random.randn(yy.shape[0])
    ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(numpy.fft.fft(yy))
    # plt.plot(Fyy[1:])
    # plt.show()
    guess_index = numpy.argmax(Fyy[4:len(Fyy)//2])+4
    guess_freq = abs(ff[guess_index]+4)   # excluding the zero frequency "peak", which is related to offset
    print(guess_index)
    guess_amp = numpy.std(yy) * 2.**0.5
    guess_offset = numpy.mean(yy)
    guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, np.random.randn(),
                        #  np.random.randn(), 2.*numpy.pi*guess_freq, -0.01,
                        #  np.random.randn(), 2.*numpy.pi*guess_freq, +0.01,
                        numpy.mean(yy[:len(yy)//2]) - numpy.mean(yy[len(yy)//2:]) / (len(yy)//2), 
                        guess_offset])

    def sinfunc(t, 
                A1, w1, p1, 
                # A2, w2, p2,
                # A3, w3, p3, 
                k, c):  return (A1 * numpy.sin(w1*t + p1) + 
                                # A2 * numpy.sin(w2*t + p2) +
                                # A3 * numpy.sin(w3*t + p3) +
                                k*t + c)
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    (A1, w1, p1,
    #  A2, w2, p2, 
    #  A3, w3, p3,
    k, c) = popt
    
    fitfunc = lambda t: sinfunc(t, *popt)
    loss = np.sum(np.abs(np.array([fitfunc(t) for t in tt]) -  yy_))

    fitfunc = lambda t: sinfunc(t, *popt)
    return {"loss": loss, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}

def fit_sin_base2(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = numpy.array(tt)
    yy_ = [yyy for yyy in yy]
    yy = numpy.array(yy_)

    yy = numpy.array(yy)
    # if np.random.randn() > 0.5:
    #     yy += np.random.randn(yy.shape)
    ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(numpy.fft.fft(yy))
    # plt.plot(Fyy[1:])
    # plt.show()
    guess_index = numpy.argmax(Fyy[4:len(Fyy)//2])+4
    guess_freq = abs(ff[guess_index]+4)   # excluding the zero frequency "peak", which is related to offset
    print(guess_index)
    guess_amp = numpy.std(yy) * 2.**0.5
    guess_offset = numpy.mean(yy)
    guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, np.random.randn(),
                         np.random.randn(), 2.*numpy.pi*guess_freq, -0.01,
                        #  np.random.randn(), 2.*numpy.pi*guess_freq, +0.01,
                        numpy.mean(yy[:len(yy)//2]) - numpy.mean(yy[len(yy)//2:]) / (len(yy)//2), 
                        guess_offset])

    def sinfunc(t, 
                A1, w1, p1, 
                A2, w2, p2,
                # A3, w3, p3, 
                k, c):  return (A1 * numpy.sin(w1*t + p1) + 
                                A2 * numpy.sin(w2*t + p2) +
                                # A3 * numpy.sin(w3*t + p3) +
                                k*t + c)
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    (A1, w1, p1,
     A2, w2, p2, 
    #  A3, w3, p3,
    k, c) = popt
    
    fitfunc = lambda t: sinfunc(t, *popt)
    loss = np.sum(np.abs(np.array([fitfunc(t) for t in tt]) -  yy_))

    fitfunc = lambda t: sinfunc(t, *popt)
    return {"loss": loss, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}


def fit_sin_base3(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = numpy.array(tt)
    yy_ = [yyy for yyy in yy]
    yy = numpy.array(yy_)

    yy = numpy.array(yy)
    # if np.random.randn() > 0.5:
    #     yy += np.random.randn(yy.shape)
    ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(numpy.fft.fft(yy))
    # plt.plot(Fyy[1:])
    # plt.show()
    guess_index = numpy.argmax(Fyy[4:len(Fyy)//2])+4
    guess_freq = abs(ff[guess_index]+4)   # excluding the zero frequency "peak", which is related to offset
    print(guess_index)
    guess_amp = numpy.std(yy) * 2.**0.5
    guess_offset = numpy.mean(yy)
    guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, np.random.randn(),
                         np.random.randn(), 2.*numpy.pi*guess_freq*np.random.uniform(), -0.01,
                         np.random.randn(), 2.*numpy.pi*guess_freq*2*np.random.uniform(), +0.01,
                        numpy.mean(yy[:len(yy)//2]) - numpy.mean(yy[len(yy)//2:]) / (len(yy)//2), 
                        guess_offset])

    def sinfunc(t, 
                A1, w1, p1, 
                A2, w2, p2,
                A3, w3, p3, 
                k, c):  return (A1 * numpy.sin(w1*t + p1) + 
                                A2 * numpy.sin(w2*t + p2) +
                                A3 * numpy.sin(w3*t + p3) +
                                k*t + c)
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    (A1, w1, p1,
     A2, w2, p2, 
     A3, w3, p3,
    k, c) = popt
    
    fitfunc = lambda t: sinfunc(t, *popt)
    loss = np.sum(np.abs(np.array([fitfunc(t) for t in tt]) -  yy_))

    fitfunc = lambda t: sinfunc(t, *popt)
    return {"loss": loss, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}


def optimise_case(arr_in, casenum = 1):

    larger_range = 1099

    yy = arr_in
    tt = range(len(yy))


    if casenum == 1:
        res = fit_sin_base(tt,yy)
    else:
        randnum = np.random.randn()
        if randnum < 0.2:
            res = fit_sin_base(tt,yy)
        elif randnum < 0.2:
            res = fit_sin_base2(tt,yy)
        else:
            res = fit_sin_base3(tt,yy)

    

    # plt.plot(tt, yy, "-k", label="y", linewidth=2)
    # # plt.plot(tt, diff, label="y", linewidth=2)
    # plt.plot(tt, res["fitfunc"](tt), "r-", label="y fit curve", linewidth=2)
    # plt.legend(loc="best")
    # plt.show()

    preds = list(res["fitfunc"](range(larger_range)))
    moves = [a>b for a,b in zip(preds[1:],preds[:-1])]
    answer = []
    for i,_ in enumerate(moves[:-1]):
        if moves[i] != moves[i+1]:
            if moves[i]:
                answer.append(i)
            else:
                answer.append(-i)

    # plt.figure(figsize=(14,3))
    # plt.plot(tt, yy, "-k", label="y", linewidth=2)
    # plt.plot(range(larger_range), res["fitfunc"](range(larger_range)), "r-", label="y fit curve", linewidth=2)
    # plt.legend(loc="best")
    # for xc in answer:
    #     if xc > 0 and xc < 200:
    #         plt.axvline(x=xc+1)
    # plt.show()

    ans = []
    for a in answer:
        if abs(a) > 100:
            ans.append(a)
    if ans[0] > 0:
        del ans[0]
    # no need to fix the end

    ans = [abs(a) for a in ans]

    # plt.figure(figsize=(14,3))
    # plt.plot(tt, yy, "-k", label="y", linewidth=2)
    # plt.plot(range(larger_range), res["fitfunc"](range(larger_range)), "r-", label="y fit curve", linewidth=2)
    # plt.legend(loc="best")
    # for xc in ans:
    #     if xc > 0 and xc < 200:
    #         plt.axvline(x=xc+1)
    # plt.show()
    
    return {"ans" : ans, "loss": res["loss"]}





    
























































# def optimise_case1(arr_in):

#     def fit_sin_base(tt, yy):
#         '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
#         tt = numpy.array(tt)
#         yy = numpy.array(yy)
#         ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
#         Fyy = abs(numpy.fft.fft(yy))
#         # plt.plot(Fyy[1:])
#         # plt.show()
#         guess_index = numpy.argmax(Fyy[2:len(Fyy)//2])+2
#         guess_freq = abs(ff[guess_index]+2)   # excluding the zero frequency "peak", which is related to offset
#         print(guess_index)
#         guess_amp = numpy.std(yy) * 2.**0.5
#         guess_offset = numpy.mean(yy)
#         guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, +0.01,
#     #                          guess_amp, 2.*numpy.pi*guess_freq, -0.01,
#     #                          guess_amp, 2.*numpy.pi*guess_freq, 0.,
#                             numpy.mean(yy[:len(yy)//2]) - numpy.mean(yy[len(yy)//2:]) / (len(yy)//2), 
#                             guess_offset])

#         def sinfunc(t, 
#                     A1, w1, p1, 
#     #                 A2, w2, p2,
#     #                 A3, w3, p3, 
#                     k, c):  return (A1 * numpy.sin(w1*t + p1) + 
#     #                                 A2 * numpy.sin(w2*t + p2) +
#     #                               A3 * numpy.sin(w3*t + p3) +
#                                     k*t + c)
#         popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
#         (A1, w1, p1,
#     #      A2, w2, p2, 
#     #      A3, w3, p3,
#         k, c) = popt

#         fitfunc = lambda t: sinfunc(t, *popt)
#         return {"fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}


#     larger_range = 1099

#     yy = arr_in
#     tt = range(len(yy))
#     res = fit_sin_base(tt,yy)
#     res

#     # plt.plot(tt, yy, "-k", label="y", linewidth=2)
#     # # plt.plot(tt, diff, label="y", linewidth=2)
#     # plt.plot(tt, res["fitfunc"](tt), "r-", label="y fit curve", linewidth=2)
#     # plt.legend(loc="best")
#     # plt.show()

#     preds = list(res["fitfunc"](range(larger_range)))
#     moves = [a>b for a,b in zip(preds[1:],preds[:-1])]
#     answer = []
#     for i,_ in enumerate(moves[:-1]):
#         if moves[i] != moves[i+1]:
#             if moves[i]:
#                 answer.append(i)
#             else:
#                 answer.append(-i)

#     # plt.figure(figsize=(14,3))
#     # plt.plot(tt, yy, "-k", label="y", linewidth=2)
#     # plt.plot(range(larger_range), res["fitfunc"](range(larger_range)), "r-", label="y fit curve", linewidth=2)
#     # plt.legend(loc="best")
#     # for xc in answer:
#     #     if xc > 0 and xc < 200:
#     #         plt.axvline(x=xc+1)
#     # plt.show()

#     ans = []
#     for a in answer:
#         if abs(a) > 100:
#             ans.append(a)
#     if ans[0] > 0:
#         del ans[0]
#     # no need to fix the end

#     ans = [abs(a) for a in ans]

#     # plt.figure(figsize=(14,3))
#     # plt.plot(tt, yy, "-k", label="y", linewidth=2)
#     # plt.plot(range(larger_range), res["fitfunc"](range(larger_range)), "r-", label="y fit curve", linewidth=2)
#     # plt.legend(loc="best")
#     # for xc in ans:
#     #     if xc > 0 and xc < 200:
#     #         plt.axvline(x=xc+1)
#     # plt.show()

#     return ans



