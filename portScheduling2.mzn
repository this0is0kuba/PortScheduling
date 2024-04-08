include "globals.mzn"; 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

int: nsh;
set of int: Ship = 1..nsh;
set of int: Ship_Length = 1..max(ship_length);
set of int: Ship_Width = 1..max(ship_width);
array[Ship] of int: ship_size;
array[Ship] of int: load_goods;

int: maxtime;
set of int: Time = 0..maxtime;
array[Ship] of Time: arrival;

int: ship_types_number;
set of int: Ship_Types = 1..ship_types_number;
array[Ship_Types] of int: ship_speed;
array[Ship_Types] of int: ship_width;
array[Ship_Types] of int: ship_length;

int: reclaim_time;

int: nr;
int: nre;
set of int: Rail = 1..nr;
set of int: Reclaimer = 1..nre;
set of int: Position_Length = 1..max(platform_length);
array[Rail] of int: platform_length;
array[Rail] of int: platform_time;
array[Rail] of int: reclaimers_number;
array[Reclaimer] of int: reclaimers_platform;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VARIABLES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% which -> rails assosiated with ships
% ship_position -> assigned location for ship
% start -> when the ship arrives to the platform
% finished -> when the ship will be empty
% leaved -> when the ships start leaving the port
% ship_status -> true if ship is empty

array[Ship] of var Rail: which;
array[Ship] of var Position_Length: ship_position; 
array[Ship] of var Time: start; 
array[Ship] of var Time: finished;
array[Ship] of var Time: leaved;

array[Ship, Time] of var bool: ship_status;

array[Ship, Time] of var 0..max(ship_length): used_reclaimers_by_ship;
array[Rail, Time] of var 0..max(reclaimers_number): free_reclaimers;
array[Ship, Time] of var int: total_working_time;

array[Reclaimer, Time] of var 1..max(platform_length): reclaimers_position;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PREDICATS AND FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% add constraint to prevent big ships arrive in each place at the port
predicate enough_space_for_ship(var Ship: s) = 
  ship_position[s] + ship_length[ship_size[s]] <= platform_length[which[s]];
  
predicate not_overlape_ships(var Ship: s1, var Ship: s2) =  
    (
      ship_position[s1] + ship_length[ship_size[s1]] < ship_position[s2] 
        \/ 
      ship_position[s2] + ship_length[ship_size[s2]] < ship_position[s1] 
    );

predicate equality_of_reclaimers(var Rail: r, var Time: t) = 
  free_reclaimers[r, t] = reclaimers_number[r] - sum([used_reclaimers_by_ship[s, t] | s in Ship where which[s] = r]);

function var int: ship_time(var Ship: s) =
  platform_time[which[s]] div ship_speed[ship_size[s]];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CONSTRAINTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Time Constraints

constraint forall(s in Ship) (
  start[s] >= arrival[s] + ship_time(s)
);

constraint forall(s in Ship) (
  finished[s] = min([t | t in Time where ship_status[s, t]])
);

constraint forall(s in Ship) (
  leaved[s] >= finished[s]
);

%%%%% Ship Constraints %%%%%

constraint forall(s in Ship) (enough_space_for_ship(s));

constraint forall(
  s1, s2 in Ship
  where s1 != s2 /\ which[s1] = which[s2] /\ start[s2] < leaved[s1] /\ leaved[s2] > start[s1]
) (
  not_overlape_ships(s1, s2)
);

% redundant constraint
constraint forall(s in Ship) (
  ship_position[s] mod 5 == 1
);

% redundant constraint
constraint forall(s in Ship, t in 0..maxtime-1 where ship_status[s, t]) (
  ship_status[s, t+1] = ship_status[s, t]
);

%%%%% Reclaimer Constraint %%%%%

constraint forall(r in Rail, t in Time) (
  equality_of_reclaimers(r, t)
);

constraint forall(s in Ship, t in Time) (
  used_reclaimers_by_ship[s, t] <= ship_length[ship_size[s]]
);

constraint forall(s in Ship, t in Time where t < start[s]) (
  used_reclaimers_by_ship[s, t] = 0
);

% redundant constraint
constraint forall(s in Ship, t in 1..maxtime where t >= finished[s] + 1) (
  used_reclaimers_by_ship[s, t] = 0
);

constraint forall(s in Ship, t in 0..maxtime-1) (
  total_working_time[s, t + 1] = total_working_time[s, t] + used_reclaimers_by_ship[s, t + 1]
);

constraint forall(s in Ship) (
   total_working_time[s, 0] = 0 
);

constraint forall(r in Rail, t in Time) (
   increasing([reclaimers_position[rec, t] | rec in Reclaimer where r = reclaimers_platform[rec]])
);

constraint forall(r in Rail, t in Time) (
   alldifferent([reclaimers_position[rec, t] | rec in Reclaimer where r = reclaimers_platform[rec]])
);

constraint forall(rec in Reclaimer, t in Time) (
  reclaimers_position[rec, t] <= platform_length[reclaimers_platform[rec]]
);

constraint forall(s in Ship, t in Time where t >= start[s] /\ t < finished[s]) (
  used_reclaimers_by_ship[s, t] = 
    sum([
        1 | rec in Reclaimer 
        where 
          reclaimers_platform[rec] = which[s] /\
          reclaimers_position[rec, t] >= ship_position[s] /\ 
          reclaimers_position[rec, t] <= ship_position[s] + ship_length[ship_size[s]]   
      ])
);

%%%%% Connections %%%%%

constraint forall(s in Ship, t in 0..maxtime-1) (
  ship_status[s, t + 1] = 
    ((total_working_time[s, t] div reclaim_time) = ship_length[ship_size[s]] * ship_width[ship_size[s]])
);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBJECTIVE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

var int: obj = sum([leaved[s] - arrival[s] | s in Ship]);

% solve satisfy;
solve minimize obj;

output
["which: ", show(which), ";\n"] ++
["ship_position: ", show(ship_position), ";\n"] ++
["arrival: ", show(arrival), ";\n"] ++
["start: ", show(start), ";\n"] ++
["finished: ", show(finished), ";\n"] ++
["leaved: ", show(leaved), ";\n"] ++
% ["ship status: ", show([ship_status[1,t] | t in Time]), ";\n"] ++
["obj: ", show(obj), ";\n"] ++

% aux
% ["reclaimers_position: ", show([reclaimers_position[r, 2] | r in Reclaimer where reclaimers_platform[r] = 8]), ";\n"] ++ 
% ["free_reclaimers: ", show([free_reclaimers[1, t] | t in Time]), ";\n"] ++
% ["used_reclaimers_by_ship: ", show([used_reclaimers_by_ship[1, t] | t in Time]), ";\n"] ++
% ["total_working_time: ", show([total_working_time[1, t] | t in Time]), ";\n"] ++

[];
