"""
cost_model.py
-------------
Daily cost-benefit model for converting a commercial vehicle from petrol to CNG.

Structure follows docs/model_inputs.md ("Cost model structure"):

    fuel saving per day  - what the driver stops spending on fuel
    queue cost per day   - earnings lost while waiting at a CNG station
    loan cost per day    - repaying a loan taken out for the conversion
    net benefit per day  = fuel saving - queue cost - loan cost

Design choice: no numbers live inside these functions. Every price, rate and
time is passed in as an argument, so the same functions can run the low / mid /
high scenarios from data/raw/model_inputs.csv (or survey data later) without
editing this file. Only the example at the bottom uses specific values, and
each one is tagged with its source ID from docs/sources.md.

Run from the project root to see a worked example:
    python src/cost_model.py
"""


def fuel_saving_per_day(petrol_spend_per_day, petrol_price, cng_price, efficiency_ratio=1.0):
    """
    Naira saved on fuel per day by switching from petrol to CNG.

    In plain words: work out what the same day's driving would cost on CNG,
    then subtract it from what the driver spends on petrol now.

        CNG cost per day = petrol spend x (CNG price / petrol price) / efficiency ratio
        fuel saving      = petrol spend - CNG cost per day

    Why this works: petrol spend / petrol price = litres used. If 1 scm of CNG
    goes as far as 1 litre (efficiency_ratio = 1.0), the driver needs the same
    number of scm, each costing the CNG price. If CNG goes further
    (ratio > 1), fewer scm are needed, so the CNG cost is divided by the ratio.

    Args:
        petrol_spend_per_day: naira per day currently spent on petrol
        petrol_price:         naira per litre
        cng_price:            naira per standard cubic metre (scm)
        efficiency_ratio:     (km per scm of CNG) / (km per litre of petrol), no
                              unit. 1.0 = equal distance, which docs/model_inputs.md
                              finds is roughly true (conflict C4).

    Returns:
        Fuel saving in naira per day.
    """
    cng_cost_per_day = petrol_spend_per_day * (cng_price / petrol_price) / efficiency_ratio
    return petrol_spend_per_day - cng_cost_per_day


def queue_cost_per_day(refuels_per_day, queue_hours, earnings_per_hour):
    """
    Naira of earnings lost per day while queuing for CNG.

    In plain words: every hour in a queue is an hour the driver is not carrying
    passengers, so it costs them what they would have earned in that hour.

        queue cost = refuels per day x hours per queue x earnings per hour

    Args:
        refuels_per_day:   number of CNG refuels per day (a fraction such as
                           0.5 means one refuel every two days)
        queue_hours:       hours spent waiting per refuel
        earnings_per_hour: naira per hour the driver would earn instead (net of
                           owner remittance and app commission)

    Returns:
        Queue cost in naira per day.
    """
    return refuels_per_day * queue_hours * earnings_per_hour


def loan_cost_per_day(conversion_cost, annual_interest_rate, tenor_years, working_days_per_year=312):
    """
    Naira per working day needed to repay a conversion loan.

    In plain words: a standard loan is repaid in equal monthly instalments that
    cover interest plus part of the original amount. We take that monthly
    payment, turn it into a yearly total, and spread it over the days the
    driver actually works.

        monthly rate    = annual interest rate / 12
        months          = tenor years x 12
        monthly payment = cost x monthly rate / (1 - (1 + monthly rate) ^ -months)
        daily cost      = monthly payment x 12 / working days per year

    Special cases:
        - interest rate of 0: no interest, so monthly payment = cost / months
          (the formula above would divide by zero)
        - conversion cost of 0 (e.g. a free, subsidised kit): returns 0

    Note: the daily cost applies only while the loan is being repaid
    (tenor_years). After that it drops to zero.

    Args:
        conversion_cost:       naira borrowed for the conversion
        annual_interest_rate:  decimal per year (17.5% -> 0.175, not 17.5)
        tenor_years:           years to repay
        working_days_per_year: days driven per year. Default 312 = 6 days a week
                               x 52 weeks, an assumption until survey data is in.

    Returns:
        Loan repayment in naira per working day.
    """
    if conversion_cost == 0:
        return 0.0

    months = tenor_years * 12

    if annual_interest_rate == 0:
        monthly_payment = conversion_cost / months
    else:
        monthly_rate = annual_interest_rate / 12
        monthly_payment = conversion_cost * monthly_rate / (1 - (1 + monthly_rate) ** -months)

    return monthly_payment * 12 / working_days_per_year


def net_benefit_per_day(fuel_saving, queue_cost, loan_cost):
    """
    Naira per day the driver is better off (or worse off, if negative) on CNG.

        net benefit = fuel saving - queue cost - loan cost

    Args:
        fuel_saving: naira per day, from fuel_saving_per_day()
        queue_cost:  naira per day, from queue_cost_per_day()
        loan_cost:   naira per day, from loan_cost_per_day()

    Returns:
        Net benefit in naira per day. Positive = CNG pays off.
    """
    return fuel_saving - queue_cost - loan_cost


def break_even_queue_hours(fuel_saving, loan_cost, refuels_per_day, earnings_per_hour):
    """
    The queue length (hours per refuel) at which CNG stops paying off.

    In plain words: what is left of the fuel saving after the loan repayment is
    the most a driver can afford to lose in queues. Dividing that by what each
    queue hour costs (refuels x earnings per hour) gives the longest queue
    the driver can tolerate. This is the study's headline metric.

        break-even hours = (fuel saving - loan cost) / (refuels per day x earnings per hour)

    Set net_benefit_per_day() to zero and solve for queue hours to get this.

    Args:
        fuel_saving:       naira per day
        loan_cost:         naira per day
        refuels_per_day:   refuels per day
        earnings_per_hour: naira per hour

    Returns:
        Break-even queue time in hours per refuel. Returns 0 if the loan cost
        alone already wipes out the fuel saving (CNG doesn't pay off even with
        no queue at all).
    """
    hours = (fuel_saving - loan_cost) / (refuels_per_day * earnings_per_hour)
    return max(hours, 0.0)


def payback_days(conversion_cost, fuel_saving, queue_cost):
    """
    Working days for a driver who pays cash to recover the conversion cost.

    In plain words: each day the driver keeps (fuel saving - queue cost). Divide
    the conversion cost by that daily gain to see how many days it takes to
    earn the money back. No loan here, because the driver paid upfront.

        payback days = conversion cost / (fuel saving - queue cost)

    Args:
        conversion_cost: naira paid upfront
        fuel_saving:     naira per day
        queue_cost:      naira per day

    Returns:
        Payback period in working days, or None if queue costs eat the whole
        fuel saving (daily gain is zero or negative), so it never pays back.
    """
    daily_gain = fuel_saving - queue_cost
    if daily_gain <= 0:
        return None
    return conversion_cost / daily_gain


if __name__ == "__main__":
    # -----------------------------------------------------------------------
    # Worked example: a Lagos ride-hailing car.
    # Source IDs refer to docs/sources.md; all values also appear in
    # data/raw/model_inputs.csv (mid scenario unless noted).
    # -----------------------------------------------------------------------
    petrol_spend = 20_000        # NGN/day, ridehail_daily_fuel_petrol (S21, pre-2026 prices)
    petrol_price = 1_400         # NGN/litre, petrol_price_national mid (S11)
    cng_price = 318              # NGN/scm, cng_price car mid (S11)
    queue_hours = 4              # hours per refuel, queue_time_per_refuel mid (S02; S04)
    conversion_cost = 1_300_000  # NGN, conversion_cost car mid (S40)
    interest_rate = 0.175        # 17.5%/yr, loan_interest_rate mid (S18)
    tenor_years = 2              # years, loan_tenor mid (S18)

    # ASSUMPTIONS, not sourced: earnings per hour and refuels per day are
    # placeholders until the driver survey provides real values
    # (docs/model_inputs.md, "Data gaps addressed by the driver survey").
    refuels_per_day = 1
    earnings_per_hour = 3_000    # NGN/hour
    working_days = 312           # days/yr = 6 days x 52 weeks, also an assumption

    saving = fuel_saving_per_day(petrol_spend, petrol_price, cng_price)
    queue = queue_cost_per_day(refuels_per_day, queue_hours, earnings_per_hour)
    loan = loan_cost_per_day(conversion_cost, interest_rate, tenor_years, working_days)
    net = net_benefit_per_day(saving, queue, loan)
    break_even = break_even_queue_hours(saving, loan, refuels_per_day, earnings_per_hour)
    payback = payback_days(conversion_cost, saving, queue)

    print("Ride-hailing car: CNG conversion, daily economics")
    print("-" * 52)
    print(f"Fuel saving per day        : NGN {saving:>10,.0f}")
    print(f"Queue cost per day         : NGN {queue:>10,.0f}")
    print(f"Loan cost per working day  : NGN {loan:>10,.0f}  (for {tenor_years} years)")
    print(f"Net benefit per day        : NGN {net:>10,.0f}")
    print(f"Break-even queue time      : {break_even:.2f} hours per refuel  (assumed queue: {queue_hours} h)")
    if payback is None:
        print("Payback (cash, no loan)    : never - queue cost exceeds fuel saving")
    else:
        print(f"Payback (cash, no loan)    : {payback:,.0f} working days "
              f"(~{payback / working_days:.1f} years at {working_days} days/yr)")
