%%%%%%%%%%%%%%%%%%%%%%%%%%%%% INPUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

int: nsh;
set of int: Ship = 1..nsh;
set of int: Ship_Length = 1..max(ship_length);
set of int: Ship_Width = 1..max(ship_width);
array[Ship] of int: ship_width;
array[Ship] of int: ship_length;
array[Ship] of int: ship_size;
array[Ship] of int: load_goods;

int: maxtime;
set of int: Time = 0..maxtime;
array[Ship] of Time: arrival;

int: ship_types_number;
set of int: Ship_Types = 1..ship_types_number;
array[Ship_Types] of int: ship_speed;

int: reclaim_time;
int: move_time;
int: car_time;
int: take_time;

int: nr;
int: nre;
set of int: Rail = 1..nr;
set of int: Reclaimer = 1..nre;
set of int: Position_Length = 1..max(platform_length);
set of int: Position_Width = 1..max(platform_width);
array[Rail] of int: platform_length;
array[Rail] of int: platform_width;
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

array[Reclaimer, Time] of var Position_Length: reclaimer_position;
array[Rail, Position_Length, Time] of var bool: is_reclaimer;

array[Ship, Ship_Length, Time] of var 0..max(ship_width): container_ship_position;
array[Rail, Position_Width, Position_Length, Time] of var bool: container_platform_position;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PREDICATS AND FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% add constraint to prevent big ships arrive in each place at the port
predicate enough_space_for_ship(var Ship: s) = 
  ship_position[s] + ship_length[s] <= platform_length[which[s]];
  
predicate not_overlape_ships(var Ship: s1, var Ship: s2) =  
    (
      ship_position[s1] + ship_length[s1] < ship_position[s2] 
        \/ 
      ship_position[s2] + ship_length[s2] < ship_position[s1] 
    );

predicate not_overlape_reclaimers(var Reclaimer: r1, var Reclaimer: r2) = 
       forall(t in Time) (reclaimer_position[r1, t] < reclaimer_position[r2, t]);
       
predicate constraint_containers_on_ship(var Ship: s, var Ship_Length: sl, 
                                       var 0..maxtime-reclaim_time: t) =
   container_ship_position[s, sl, t+reclaim_time] = container_ship_position[s, sl, t] - 1;

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

% Ship Constraints

constraint forall(s in Ship) (enough_space_for_ship(s));

constraint forall(
  s1, s2 in Ship
  where s1 != s2 /\ which[s1] = which[s2] /\ start[s2] <= leaved[s1] /\ leaved[s2] >= start[s1]
) (
  not_overlape_ships(s1, s2)
);

constraint forall(s in Ship, t in Time) (
  ship_status[s, t] = 
  (
    sum(
      [container_ship_position[s, sl, t] | 
       sl in Ship_Length where sl <= ship_length[s]]
    ) = 0
  )
);

constraint forall(s in Ship, t in 0..maxtime-1 where ship_status[s, t]) (
  ship_status[s, t+1] = ship_status[s, t]
);

% Reclaimer Constraints

% channel two arrays
constraint forall(r in Reclaimer, t in Time) (
  is_reclaimer[reclaimers_platform[r], reclaimer_position[r, t], t] = true
);

% channel two arrays
constraint forall(r in Rail, t in Time) (
   count([is_reclaimer[r, l, t] | l in Position_Length]) = reclaimers_number[r]
);

constraint forall (r in Reclaimer, t in Time) (
  reclaimer_position[r, t] <= platform_length[reclaimers_platform[r]]
);

constraint forall(
  r1, r2 in Reclaimer 
  where r1 < r2 /\ reclaimers_platform[r1] = reclaimers_platform[r2]
) (
  not_overlape_reclaimers(r1, r2)
);

% Container Constraints

% Before ships come to port they have containers
constraint forall (
  s in Ship, sw in Ship_Width, sl in Ship_Length, t in Time  
  where t <= start[s] /\ sw <= ship_width[s] /\ sl <= ship_length[s]
) (
  container_ship_position[s, sl, t] = ship_width[s]
);

constraint forall (
  s in Ship, sl in Ship_Length, t in 0..maxtime-reclaim_time 
  where t >= start[s] /\ sl <= ship_length[s] 
        /\  
        container_platform_position[which[s], 1, sl + ship_position[s] - 1, t] = false
        /\
        forall(rt in 0..reclaim_time-1) (is_reclaimer[which[s], sl + ship_position[s] - 1, t + rt])
) (
  constraint_containers_on_ship(s, sl, t)
);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OBJECTIVE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

var int: obj = sum([leaved[s] - arrival[s] | s in Ship]);

solve satisfy;
% solve minimize obj;

output
["which: ", show(which), ";\n"] ++
["ship_position: ", show(ship_position), ";\n"] ++
["arrival: ", show(arrival), ";\n"] ++
["start: ", show(start), ";\n"] ++
["finished: ", show(finished), ";\n"] ++
["leaved: ", show(leaved), ";\n"] ++
% ["reclaimer position: ", show(reclaimer_position), ";\n"] ++
["ship status: ", show([ship_status[1,t] | t in Time]), ";\n"] ++
["obj: ", show(obj), ";\n"] ++

% aux

% ["help: ", show([sum(
%       [container_ship_position[1, sl, t] | 
%        sw in Ship_Width, sl in Ship_Length where sw <= ship_width[1] /\ sl <= ship_length[1]]
%     ) | t in Time])] ++

["number of: ", show([container_ship_position[1, sl, 3] | sl in Ship_Length where sl <= ship_length[1]]), ";\n"] ++
["number of: ", show([container_ship_position[1, sl, 4] | sl in Ship_Length where sl <= ship_length[1]]), ";\n"] ++
["number of: ", show([container_ship_position[1, sl, 5] | sl in Ship_Length where sl <= ship_length[1]]), ";\n"] ++


[];
