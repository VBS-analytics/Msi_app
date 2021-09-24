function update_state_date_picker(use_curr_date,date_pick) {
    if (use_curr_date.length < 1) {
        return false, date_pick
    } else {
        return true, null
    }
}