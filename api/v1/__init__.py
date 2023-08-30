def calc_tot_rate(user_id):
    user = storage.get(User, user_id)
    _session = storage.session()
    reviews = _session.query(Review).filter(Review.for_user_id==user_id)
    total = 0
    count = 0
    for review in reviews:
        total += review.rating
        count += 1
    rate_tot = total / count
    user.rating = rate_tot
    storage.save
