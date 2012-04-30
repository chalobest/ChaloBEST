from mumbai.models import *
import pdb
# FIXME: UniqueRoute stringification, routes 314 and 9

def fix_distances():
    for unique_route in UniqueRoute.objects.all():
        # RouteDetail sometimes isn't in order from from_stop to to_stop
        from_stop, to_stop = unique_route.from_stop.id, unique_route.to_stop.id
        details = list(unique_route.route.routedetail_set.all())
        # Sometimes to_stop comes before from_stop in RouteDetail. What is there to say.
        # so reverse the list if that happens.. so a from_stop will always come before a to_stop
        for detail in details:
            if detail.stop.id == from_stop.id: break
            if detail.stop.id == to_stop.id:
                details.reverse()
                break

        # setup vars
        distance = 0.0
        record = False
        last_stop_passed = False

        for detail in details:
            # basic idea, run thru each detail, 
            # if it has km info, then add it, 
            # if to_stop reached, and if it did not have km info, 
            # then go to the next detail having km info add it and done.

            # For route 240RING, some detail.km is null???            
            # distance > 0 because of 100RING returning 1 stop shy of its start       
            if distance > 0 and detail.stop.id == to_stop:
                last_stop_passed = True

            # is a stage
            if record:
                if not last_stop_passed: 
                    # add it
                    if detail.km:
                        distance += float(detail.km)                    
                else:
                    # if stage having km info reached after last stop, then add and exit loop
                    if detail.km:
                        distance += float(detail.km)
                    record=False
                    last_stop_passed = True
                    break

            #if record and distance > 0 and detail.stop.id == to_stop:
            #    record = False
            #    break


            # Start recording *after* we check for the break, because,
            # if from_stop == to_stop, we don't want to break on the first stop
            if detail.stop.id == from_stop: record = True

        if record:
            #pdb.set_trace()
            print Exception("UniqueRoute %d: %s from %s to %s ran off the end while measuring distance!" %(unique_route.id, unique_route, unique_route.from_stop.code, unique_route.to_stop.code))
        if not distance:
            print Exception("UniqueRoute %d: %s from %s to %s still has no distance!" % (unique_route.id, unique_route, unique_route.from_stop.code, unique_route.to_stop.code))

        #if distance > float(unique_route.distance):
        if not unique_route.distance:
            unique_route.distance = distance
            unique_route.save()

columns = ["runtime%d" % n for n in range(1,5)]
def fix_missing_runtimes():
    for schedule in RouteSchedule.objects.all():
        # other schedules for the same unique route (but at different times)
        sibling_schedules = schedule.unique_route.routeschedule_set.all()
        # the "full" schedules for this route are used to attempt to
        # guesstimate the schedules of partial subroutes
        related_routes = related_schedules = []
        related_subroutes = list(schedule.unique_route.route.uniqueroute_set.all())

        # the main inner loop: for each runtime column ---
        for col_idx, column in enumerate(columns):
            # if the runtime is set, AWESOME, bail
            if getattr(schedule, column): continue

            # try to use the previous column....if available
            if getattr(schedule, column): continue
            if col_idx > 0:
                prev_runtime = getattr(schedule, columns[col_idx-1])
                if prev_runtime:
                    setattr(schedule, column, prev_runtime)
                    schedule.save()
                    continue

            # ... or the next column, if it comes to that.
            if col_idx < len(columns)-1:
                next_runtime = getattr(schedule, columns[col_idx+1])
                if next_runtime:
                    setattr(schedule, column, next_runtime)
                    schedule.save()
                    continue

            # otherwise, go through the other schedules for this subroute and
            # see if we get a matching runtime -- if so, use it
            for sibling in sibling_schedules:
                sibling_runtime = getattr(sibling, column)
                if sibling_runtime:
                    setattr(schedule, column, sibling_runtime)
                    schedule.save()
                    # print "OK  fix_missing_runtimes: %s %s fixed to %s" % (schedule, column, sibling)
                    break

            if getattr(schedule, column): continue
            # otherwise, go through the matching schedules for the full-length versions of this
            # route and extrapolate the runtime.
            if related_subroutes:
                # first, try to get the schedules for the full routes, given the same schedule type
                related_schedules = []
                for related_route in related_subroutes:
                    related_schedules += list(related_route.routeschedule_set.filter(schedule_type=schedule.schedule_type))

                # iterate over them and see if we got one with the right runtime
                for related_schedule in related_schedules:
                    related_runtime = getattr(related_schedule, column)
                    if related_runtime:
                        # if so, compute the partial runtime of this schedule as the (possibly > 1.0) fraction of runtime of the other schedule by distance
                        partial_runtime = related_runtime*float(schedule.unique_route.distance)/float(related_schedule.unique_route.distance)
                        # print "OK  fix_missing_runtimes: %s %s adjusted to parent %s" % (schedule, column, related_schedule)
                        setattr(schedule, column, partial_runtime)
                        schedule.save()
                        break

                # did we find a runtime? great, use it
                if getattr(schedule, column): continue

                # failing that, try to get the schedules for the full routes, with ANY schedule type
                for related_route in related_subroutes:
                    related_schedules += list(related_route.routeschedule_set.all())

                # iterate over them and see if we got one with the right runtime
                for related_schedule in related_schedules:
                    related_runtime = getattr(related_schedule, column)
                    if related_runtime:
                        # if so, compute the partial runtime of this schedule as the (possibly > 1.0) fraction of runtime of the other schedule by distance
                        partial_runtime = related_runtime*float(schedule.unique_route.distance)/float(related_schedule.unique_route.distance)
                        # print "OK  fix_missing_runtimes: %s %s adjusted to parent %s" % (schedule, column, related_schedule)
                        setattr(schedule, column, partial_runtime)
                        schedule.save()
                        break

            if column != "runtime4":
                print Exception("ERR fix_missing_runtimes: %s STILL missing %s!" % (schedule, column))


hcolumns = ["headway%d" % n for n in range(1,6)]
def fix_missing_headways():
    for schedule in RouteSchedule.objects.all():
        # other schedules for the same unique route (but at different times)
        sibling_schedules = schedule.unique_route.routeschedule_set.all()
        # the "full" schedules for this route are used to attempt to
        # guestimate the schedules of partial subroutes
        related_routes = related_schedules = []
        related_subroutes = list(schedule.unique_route.route.uniqueroute_set.all())
        
        # the main inner loop: for each headway column ---
        for col_idx, column in enumerate(hcolumns):
            # if the headway is set, AWESOME, bail
            if getattr(schedule, column): continue
            
            # try to use the previous column....if available
            #if getattr(schedule, column): continue
            if col_idx > 0:
                prev_headway = getattr(schedule, columns[col_idx-1])
                if prev_headway:
                    setattr(schedule, column, prev_headway)
                    schedule.save()
                    continue

            # ... or the next column, if it comes to that.
            if col_idx < len(columns)-1:
                next_headway = getattr(schedule, columns[col_idx+1])
                if next_headway:
                    setattr(schedule, column, next_headway)
                    schedule.save()
                    continue

            #try any headway in the current row:
            for hcol in hcolumns:
                headway = getattr(schedule, hcol)
                if headway:
                    setattr(schedule, column, headway)
                    schedule.save()
                    break
            
            if getattr(schedule, column):
                continue
            # otherwise, go through the other schedules for this subroute and
            # see if we get a matching headway -- if so, use it
            for sibling in sibling_schedules:
                sibling_headway = getattr(sibling, column)
                if sibling_headway:
                    setattr(schedule, column, sibling_headway)
                    schedule.save()
                    # print "OK  fix_missing_headways: %s %s fixed to %s" % (schedule, column, sibling)
                    break
                
            if getattr(schedule, column): continue
            
            break_loop = False
            for sibling in sibling_schedules:
                if break_loop:
                    break
                for hcol in hcolumns:
                    headway = getattr(sibling, hcol)
                    if headway:
                        setattr(schedule, column, headway)
                        schedule.save()
                        break_loop = True
                        break
            
            
            if getattr(schedule, column):
                continue
            
            break_loop = False        
            for r in related_subroutes:
                if break_loop:
                    break
                for related_schedule in r.routeschedule_set.all():
                    if break_loop:
                        break
                    for hcol in hcolumns:
                        headway = getattr(related_schedule, hcol)
                        if break_loop:
                            break
                        if headway:
                            setattr(schedule, column, headway)
                            schedule.save()
                            break_loop = True
                            break
                                    
            
            if getattr(schedule, column):
                continue
            
            if not getattr(schedule, column):
                print Exception("All failed for schedule with id %d" % schedule.id)
                
            
            '''
            if column != "headway5":
                print Exception("ERR fix_missing_headways: %s STILL missing %s!" % (schedule, column))
            '''    
                
