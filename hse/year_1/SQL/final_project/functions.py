import psycopg2
def start_planning(year, quarter, user, pwd):    
    delete_quarter_plan_data_query = """
            delete from plan_data
            where quarterid = %s;
            """
    delete_quarter_plan_status_query = """
            delete from plan_status
            where quarterid = %s;
            """
    add_plan_status_query = """
            insert into plan_status
            (quarterid, status, modifieddatetime, author, country)
            select distinct 
            %s as quarteid, 'R' as status, 
            now() as modifieddatetime,
            %s as author, 
            countrycode as country
            from company;
            """
    generate_plan_N = """
            insert into plan_data 
            (versionid, country, quarterid, pcid, salesamt)
            select 'N' as versionid,
                l.country, 
                %s as quarterid, 
                l.pcid, 
                coalesce (r.salesamt, 0)
            from
            (select distinct 
                    c.countrycode country,
                    p.productcategoryid as pcid
                from company c
                cross join productcategory p
                order by c.countrycode, p.productcategoryid
            ) as l 
            left join
            (select distinct
                c.countrycode as country,
                categoryid as pcid,
                avg(sum(salesamt))
                over(partition by c.countrycode, quarter_yr, categoryid
                order by c.countrycode, quarter_yr, categoryid    
                )
                as salesamt
            from company_sales as cs
            join company as c on c.id=cs.cid
            where ccls in ('A', 'B') and cs."year" in (%s, %s) 
            and quarter_yr = %s
            group by c.countrycode, qr, categoryid, quarter_yr
            order by c.countrycode, categoryid
            ) as r
            on l.country = r.country and l.pcid = r.pcid
            order by l.country, l.pcid;
            """
    generate_plan_P = """
            insert into plan_data
            (versionid, country, quarterid, pcid, salesamt)
            select 
            'P' as versionid, country, quarterid , pcid, salesamt 
            from plan_data pd;
            """
    
    con = psycopg2.connect(database="2024_plans_Melnikov", 
                           user=user, password=pwd, 
                           host="localhost")
    cur = con.cursor()    
    try:
        cur.execute(delete_quarter_plan_data_query, [f"{year}.{quarter}"])
        con.commit() 
        cur.execute(delete_quarter_plan_status_query, [f"{year}.{quarter}"]) 
        con.commit() 
        cur.execute(generate_plan_N, [f"{year}.{quarter}", year-1, year-2, quarter])
        con.commit() 
        cur.execute(generate_plan_P)
        con.commit() 
        cur.execute(add_plan_status_query, [f"{year}.{quarter}", user])
        con.commit()    
    except Exception as e:
        print(e)
        con.rollback()
    cur.close()
    con.close()

def set_lock(year, quarter, user, pwd):
    qurterid = f"{year}.{quarter}"
    query = """
            update plan_status 
            set status = 'L', 
            modifieddatetime = now(),
            author = current_user
            where quarterid = %s and
            country in 
                (select country 
                from country_managers cm
                where cm.username = current_user)
            """
    con = psycopg2.connect(database="2024_plans_Melnikov", 
                           user=user, password=pwd, 
                           host="localhost")
    cur = con.cursor()
    try:
        cur.execute(query,[qurterid])
        con.commit()
    except Exception as e:
        print(e)
        con.rollback()
    cur.close()
    con.close()

def remove_lock(year, quarter, user, pwd):
    qurterid = f"{year}.{quarter}"
    query = """
            update plan_status 
            set status = 'R', 
            modifieddatetime = now(),
            author = current_user
            where quarterid = %s and
            country in 
                (select country 
                from country_managers cm
                where cm.username = current_user)
            """
    con = psycopg2.connect(database="2024_plans_Melnikov", 
                           user=user, password=pwd, 
                           host="localhost")
    cur = con.cursor()
    try:
        cur.execute(query,[qurterid])
        con.commit()
    except Exception as e:
        print(e)
        con.rollback()
    cur.close()
    con.close()

def accept_plan(year, quarter, user, pwd):
    remove_existing_plan_query = """
            delete from plan_data
            where versionid = 'A' 
            and quarterid = %s
            and country in 
                (select country 
                from country_managers cm
                where cm.username = current_user)
            """
    accept_plan_query = """
            insert into plan_data 
            (versionid, country, quarterid, pcid, salesamt)
            select 
                'A' as versionid,
                country,
                quarterid,
                pcid, 
                salesamt
            from plan_data
            where versionid = 'P' 
            and quarterid = %s
            and country in 
                (select country 
                from country_managers cm
                where cm.username = current_user)
            """
    update_plan_status_query = """
            update plan_status 
            set status = 'A', 
            modifieddatetime = now(),
            author = current_user
            where status = 'R' and
            quarterid = %s and
            country in 
                (select country 
                from country_managers cm
                where cm.username = current_user)
            """
    
    qurterid = f"{year}.{quarter}"
    con = psycopg2.connect(database="2024_plans_Melnikov", 
                           user=user, password=pwd, 
                           host="localhost")
    cur = con.cursor()
    try:
        cur.execute(remove_existing_plan_query,[qurterid])
        con.commit()
        cur.execute(accept_plan_query,[qurterid])
        con.commit()
        cur.execute(update_plan_status_query,[qurterid])
        con.commit()
        con.close()
    except Exception as e:
        print(e)
        con.rollback()
    cur.close()


psw = {'postgres': 'sql',
       'ivan': 'sql',
       'sophie': 'sql1',
       'kirill': 'sql2'}

user = 'ivan'
#start_planning(2014, 1, user, psw[user])
user = 'kirill'
#set_lock(2014,1, user, psw[user])
#remove_lock(2014,1, user, psw[user])
#user = 'sophie'
#set_lock(2014,1, user, psw[user])
#remove_lock(2014,1, user, psw[user])
user = 'kirill'
accept_plan(2014,1, user, psw[user])
user = 'sophie'
accept_plan(2014,1, user, psw[user])