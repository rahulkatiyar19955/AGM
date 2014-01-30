cmake_minimum_required( VERSION 2.8)


SET(human             "1")
SET(robot             "2")

SET(HtableObject      "3")
SET(HtableReach       "4")
SET(HtableType        "5")
SET(HtableReachable   "6")
SET(HtablePosition    "7")
SET(HtableSee         "8")
SET(HcoffeeObject     "9")
SET(HcoffeeReach      "10")
SET(HcoffeeType       "11")
SET(HcoffeeReachable  "12")
SET(HcoffeePosition   "13")
SET(HcoffeeSee        "14")
SET(HmugObject        "15")
SET(HmugReach         "16")
SET(HmugType          "17")
SET(HmugReachable     "18")
SET(HmugPosition      "19")
SET(HmugSee           "20")


SET(RtableObject      "21")
SET(RtableReach       "22")
SET(RtableType        "23")
SET(RtableReachable   "24")
SET(RtablePosition    "25")
SET(RtableSee         "26")
SET(RcoffeeObject     "27")
SET(RcoffeeReach      "28")
SET(RcoffeeType       "29")
SET(RcoffeeReachable  "30")
SET(RcoffeePosition   "31")
SET(RcoffeeSee        "32")
SET(RmugObject        "33")
SET(RmugReach         "34")
SET(RmugType          "35")
SET(RmugReachable     "36")
SET(RmugPosition      "37")
SET(RmugSee           "38")





configure_file ("world.in.xml" "world.xml")
INSTALL(FILES "world.xml" DESTINATION /tmp )
