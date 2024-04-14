def pos_input(arg_name, new_type):
    """Infinite loop that waits for positive number to be entered."""
    while True:
        try:
            i = new_type(input(f"{arg_name}: "))
        except ValueError:
            print("[X] Incorrect input")
            continue
        if i < 0:
            print("[X] Incorrect input")
            continue
        else:
            return i


def ctr(args):
    """[Total Measured Clicks / Total Measured Ad Impressions] X 100"""
    clicks, ad_impressions = args[0], args[1]
    res = None
    if clicks >= 0 and ad_impressions > 0:
        if clicks > ad_impressions:
            print("Number of clicks can't be greater than number "
                  "of ad impressions")
            return res
        res = round(clicks / ad_impressions * 100, 3)
    return res


def roi(args):
    """Return on Investment =
    [(Amount Gained – Amount Spent) / Amount Spent] X 100"""
    gain, cost = args[0], args[1]
    res = None
    if cost > 0:
        res = round((gain - cost) / cost * 100, 3)
    return res


def apt(times_list):
    """Average Page Time = [Σ(Time Spent on a Page by a User) / Number of Users]"""
    res = None
    times = [t for t in times_list if t >= 5]
    n = len(times)
    if n == 0:
        return res

    s = sum(times)
    res = round(s / n, 3)
    return res


def clv(args):
    """CLV = Average Purchase Value * Average Purchase Frequency *
     Average Customer Lifespan"""
    res = None

    total_revenue = args[0]
    purchase_quantity = args[1]
    if purchase_quantity == 0:
        print("Wrong data: purchase quantity should be greater than 0")
        return res

    unique_customers_number = args[2]
    if unique_customers_number == 0:
        print("Wrong data: number of unique customers should be greater than 0")
        return res

    average_customer_lifespan = args[3]
    if purchase_quantity < unique_customers_number:
        print("Wrong data: number of purchases can't be less"
              "than number of unique customers")
        return res
    ap_value = total_revenue / purchase_quantity
    ap_frequency = purchase_quantity / unique_customers_number

    res = ap_value * ap_frequency * average_customer_lifespan
    return res


def cr(args):
    """CR = [Total Attributed Conversion / Total Measured Clicks] X 100"""
    res = None
    number_of_conversions = args[0]
    number_of_clicks = args[1]

    if number_of_clicks <= 0:
        return res
    if number_of_conversions > number_of_clicks:
        print("Wrong Data: number of conversions can't be greater"
              " than number of ad clicks")
        return res

    res = number_of_conversions / number_of_clicks * 100
    return res


def aca(age_list):
    """Average Customer Age = [Σ(Age of Customer) / Number of Customers]\n
    Allows to differentiate whether site audience consists more of
    younger generation, of elderly people or if it is equally
    distributed amongst both.
    Doesn't help to differentiate whether most customers are of middle age
    or if there are actually approximately equal amount of young and old people"""

    res = None
    ages = [age for age in age_list if age > 0]
    n = len(ages)
    if n == 0:
        return res

    s = sum(ages)
    res = round(s / n, 3)
    return res


def rgr(args):
    """Revenue Growth Rate"""
    current_revenue = args[0]
    previous_revenue = args[1]
    res = None
    if previous_revenue != 0:
        res = round((current_revenue - previous_revenue) / previous_revenue, 3)
    return res


def lppr(args):
    """Loyalty Program Participation Rate =
    [Loyalty Transactions/Total Transactions * 100]"""
    res = None
    loyalty_transactions, total_transactions = args[0], args[1]
    if total_transactions == 0:
        return res
    if loyalty_transactions > total_transactions:
        print("Wrong Data: number of loyalty transactions can't exceed"
              "total number of transactions")
        return res
    res = loyalty_transactions / total_transactions * 100
    return res


metrics = [ctr, roi, apt, clv, cr, aca, rgr, lppr]
metrics_name = ['Click-Through Rate',
                'Return on Investment',
                'Average Page Time',
                'Customer Lifetime Value',
                'Conversion Rate',
                'Average Customer Age',
                'Revenue Growth Rate',
                'Loyalty Program Participation Rate']

for i in range(len(metrics_name)):
    print(i, metrics_name[i])

while True:
    while True:
        n = pos_input("Select metric", int)
        if n >= len(metrics_name):
            print("[X] Incorrect input")
            continue
        else:
            break

    arguments = []
    if metrics_name[n] == "Click-Through Rate":
        arguments.append(pos_input("Number of clicks", int))
        arguments.append(pos_input("Number of ad impressions", int))
    elif metrics_name[n] == "Return on Investment":
        arguments.append(pos_input("Amount Gained", float))
        arguments.append(pos_input("Amount Spent", float))
    elif metrics_name[n] == "Average Page Time":
        while True:
            try:
                arguments = (list(map(float, input("Time(s) "
                                                   "in seconds: ").split())))
            except ValueError:
                continue
            break
    elif metrics_name[n] == "Customer Lifetime Value":
        arguments.append(pos_input("Total revenue", float))
        arguments.append(pos_input("Number of purchases", int))
        arguments.append(pos_input("Number of unique_customers", int))
        arguments.append(pos_input("Average customer"
                                   " lifespan (in months)", float))
    elif metrics_name[n] == "Conversion Rate":
        arguments.append(pos_input("Total amount of "
                                   "conversion, caused by clicks", int))
        arguments.append(pos_input("Number of ad clicks", float))
    elif metrics_name[n] == "Average Customer Age":
        while True:
            try:
                arguments = (list(map(int, input("Age(s) in "
                                                 "years: ").split())))
            except ValueError:
                continue
            break
    elif metrics_name[n] == "Revenue Growth Rate":
        arguments.append(pos_input("Current revenue", int))
        arguments.append(pos_input("Previous revenue", float))
    elif metrics_name[n] == "Loyalty Program Participation Rate":
        arguments.append(pos_input("Number of loyalty "
                                   "transactions", float))
        arguments.append(pos_input("Total number of "
                                   "transactions", float))
    result = metrics[n](arguments)
    if result is None:
        print(metrics_name[n], "can't be calculated")
    else:
        print(metrics_name[n], result, sep=' = ')
