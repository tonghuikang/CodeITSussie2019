import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
import numpy, scipy.optimize
# import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)

@app.route('/technical_analysis', methods=['POST'])
def technical_analysis():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    result = []
    for ar in data:
        result.append(optimise_case(ar))

    return jsonify(result)


def optimise_case(arr_in):

    def fit_sin_base(tt, yy):
        '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
        tt = numpy.array(tt)
        yy = numpy.array(yy)
        ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
        Fyy = abs(numpy.fft.fft(yy))
        guess_freq = abs(ff[numpy.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
        guess_amp = numpy.std(yy) * 2.**0.5
        guess_offset = numpy.mean(yy)
        guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, 0., guess_offset])

        def sinfunc(t, A, w, p, c):  return A * numpy.sin(w*t + p) + c
        popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
        A, w, p, c = popt
        f = w/(2.*numpy.pi)
        fitfunc = lambda t: A * numpy.sin(w*t + p) + c
        return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}

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