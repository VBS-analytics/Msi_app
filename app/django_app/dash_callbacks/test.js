function enab_disa_filters_apply(fil_sel_drop,fil_col_names,fil_condi,trans_txt,\
    trans_multi_txt,trans_input,trans_dt_start,trans_dt_end,trans_dt_single,\
    trans_days_single,trans_current_date,logic_dropdown) {

    if (fil_sel_drop != null && fil_col_names.includes(null) != true 
        && fil_condi.includes(null) != true) {
        
        let text_area=false
        let multi_drp=false
        let single_dt=false
        let txt_box=false
        let range_dt=false
        let sys_dt_chk=false
        let single_days=false

        for (let i in fil_condi){
            if (['starts with','contains','ends with','<','<=','==','>=','>','!='].indexOf(fil_condi[i]) > -1) {
                text_area = true
                break
            }
        }

        for (let i in fil_condi){
            if (['has value(s)'].indexOf(fil_condi[i]) > -1) {
                multi_drp = true
                break
            }
        }

        for (let i in fil_condi){
            if (['days'].indexOf(fil_condi[i]) > -1) {
                single_days=true
                txt_box=true
                sys_dt_chk=true
                break
            }
        }

        for (let i in fil_condi){
            if (['before','after','equals','not'].indexOf(fil_condi[i]) > -1) {
                single_dt = true
                break
            }
        }

        for (let i in fil_condi){
            if (['range'].indexOf(fil_condi[i]) > -1) {
                range_dt = true
                break
            }
        }

        let chk = []
        let chk2 = []

        if (single_days == true && txt_box == true && sys_dt_chk == true){
            chk2.push(trans_days_single)
            chk2.push(trans_input)
            chk2.push(trans_current_date)
        }

        if (text_area == true){
            chk.push(trans_txt)
        }

        if (multi_drp == true){
            chk.push(trans_multi_txt)
        }
        if (single_dt == true){
            chk.push(trans_dt_single)
        }
        if (range_dt == true){
            chk.push(trans_dt_start)
            chk.push(trans_dt_end)
        }

        let rt=false
        let rtt=false

        let rt2=false
        let rtt2=false


        if (chk != []) {
            for (let i in chk) {

                let chk_val = []
                for (let k in i) {
                    if (k != null && k != [] && k != '') {
                        chk_val.push(true)
                    } else {
                        chk_val.push(false)
                    }
                }


                if (chk_val.every(Boolean)==true && chk_val != []) {
                    rt=true
                } else {
                    rtt=true
                }
            }

        }

        if (chk2 != []) {
            console.log(chk2)
            let z1 = []
            for (let i in chk2[0]) {
                if (i != [] && i != null && i != '') {
                    z1.push(true)
                }
            }
            for (let j in chk2[2]) {
                if (j != []) {
                    z1.push(true)
                }
            }

            let chk2_val = []
            for (let i in chk2[1]) {
                if (i != null && i != [] && i != '') {
                    chk2_val.push(true)
                } else {
                    chk2_val.push(false)
                }
            }

            if (chk2_val.every(Boolean) == true && chk2_val != [] && 
                chk2[0].length == z1.filter(Boolean).length) {
                    rt2=true
            } else {
                rtt=true
            }


            
        }

        if (rt == true && rtt == false && rt2 == false && rtt2 == false) {
            return false
        } else if (rt == false && rtt == false && rt2 == true && rtt2 == false) {
            return false
        } else if (rt == true && rtt == false && rt2 == true && rtt2 == false) {
            return false
        } else {
            return true
        }

    } else {
        return true
    }
}