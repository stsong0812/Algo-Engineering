from datetime import datetime

def time_to_minutes(time_str):
    h, m = map(int, time_str.split(':'))
    return h * 60 + m

def minutes_to_time(minutes):
    h = minutes // 60
    m = minutes % 60
    return f'{h:02d}:{m:02d}'

def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged

def invert_intervals(intervals, start, end):
    inverted = []
    prev_end = start
    for start, end in intervals:
        if start > prev_end:
            inverted.append([prev_end, start])
        prev_end = end
    if prev_end < end:
        inverted.append([prev_end, end])
    return inverted

def intersect_intervals(lists):
    intersection = lists[0]
    for intervals in lists[1:]:
        new_intersection = []
        for start1, end1 in intersection:
            for start2, end2 in intervals:
                start_max = max(start1, start2)
                end_min = min(end1, end2)
                if start_max < end_min:
                    new_intersection.append([start_max, end_min])
        intersection = new_intersection
    return intersection

def find_available_meeting_times(schedules, working_periods, duration):
    all_available_times = []
    for schedule, (login, logout) in zip(schedules, working_periods):
        busy_times = [[time_to_minutes(start), time_to_minutes(end)] for start, end in schedule]
        busy_times.append([0, time_to_minutes(login)])
        busy_times.append([time_to_minutes(logout), 24*60])
        busy_times = merge_intervals(busy_times)
        available_times = invert_intervals(busy_times, time_to_minutes(login), time_to_minutes(logout))
        all_available_times.append(available_times)
    
    common_available_times = intersect_intervals(all_available_times)
    meeting_times = [interval for interval in common_available_times if interval[1] - interval[0] >= duration]
    return [[minutes_to_time(start), minutes_to_time(end)] for start, end in meeting_times]

def read_schedules_working_periods_and_durations(file_path):
    with open(file_path, 'r') as file:
        data_sets = file.read().strip().split('\n\n')
    
    all_data = []
    for data_set in data_sets:
        lines = data_set.strip().split('\n')
        duration_of_meeting = int(lines[0])
        schedules = []
        working_periods = []
        for line in lines[1:]:
            parts = line.strip().split(';')
            working_periods.append(parts[0].split('-'))
            schedules.append([part.split('-') for part in parts[1:]])
        all_data.append((schedules, working_periods, duration_of_meeting))
    
    return all_data

def main(file_path):
    all_data = read_schedules_working_periods_and_durations(file_path)
    
    set_count = 1
    for schedules, working_periods, duration_of_meeting in all_data:
        print(f"Data Set {set_count}: Meeting Duration {duration_of_meeting} minutes")
        available_meeting_times = find_available_meeting_times(schedules, working_periods, duration_of_meeting)
        if available_meeting_times:
            for time_range in available_meeting_times:
                print(f"Available: {time_range[0]} to {time_range[1]}")
        else:
            print("No available meeting times.")
        print("-" * 40)
        set_count += 1

if __name__ == "__main__":
    file_path = 'schedules.txt' 
    main(file_path)
