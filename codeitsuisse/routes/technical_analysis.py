import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
import numpy, scipy.optimize
# import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)

@app.route('/technical-analysis', methods=['POST'])
def technical_analysis():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    result = []
    for ar in data:
        try:
            buy_sell = optimise_case(ar)
        except:
            print("aborted")
            buy_sell = [100,1099]
        result.append(buy_sell)

    return jsonify(result)


def optimise_case(arr_in):

    def fit_sin_base(tt, yy):
        '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
        tt = numpy.array(tt)
        yy = numpy.array(yy)
        ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
        Fyy = abs(numpy.fft.fft(yy))
        # plt.plot(Fyy[1:])
        # plt.show()
        guess_index = numpy.argmax(Fyy[4:])+4
        guess_freq = abs(ff[guess_index]+4)   # excluding the zero frequency "peak", which is related to offset
        print(numpy.argmax(Fyy[4:]))
        guess_amp = numpy.std(yy) * 2.**0.5
        guess_offset = numpy.mean(yy)
        guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, 0., 0.,
                            guess_amp, 2.*numpy.pi*guess_freq, 0., 0.,
    #                          guess_amp, 2.*numpy.pi*guess_freq, 0., 0.,
                            guess_offset])

        def sinfunc(t, 
                    A1, w1, p1, k1, 
                    A2, w2, p2, k2,
    #                 A3, w3, p3, k3,
                    c):  return (A1 * numpy.sin(w1*t + p1) + k1*t + 
                                A2 * numpy.sin(w2*t + p2) + k2*t +
    #                              A3 * numpy.sin(w3*t + p3) + k3*t +
                                c)
        popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
        (A1, w1, p1, k1, 
        A2, w2, p2, k2, 
    #      A3, w3, p3, k3,
        c) = popt
        
        fitfunc = lambda t: sinfunc(t, *popt)
        return {"fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}
    
    larger_range = 1099

    yy = arr_in
    tt = range(len(yy))
    res = fit_sin_base(tt,yy)
    res

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
    
    return ans