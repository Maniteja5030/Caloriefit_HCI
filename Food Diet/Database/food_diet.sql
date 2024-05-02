drop database food_diet;
create database food_diet;
use food_diet;

create table admin(
admin_id int auto_increment primary key,
username varchar(255) not null,
password varchar(255) not null
); 

create table user(
user_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null,
phone varchar(255) not null,
password varchar(255) not null,
gender varchar(255) not null,
address varchar(255) not null,
age  varchar(255) not null
); 

create table nutrition(
nutrition_id int auto_increment primary key,
name varchar(255) not null,
email varchar(255) not null,
phone varchar(255) not null,
password varchar(255) not null,
about varchar(255) not null,
picture varchar(255) not null,
status varchar(255) default 'Not Verified'
); 

create table diet(
diet_id int auto_increment primary key,
diet_title varchar(255) not null,
age_from varchar(255) not null,
age_to  varchar(255) not null,
instructions varchar(255) not null,
image varchar(255) not null,
about_diet varchar(255) not null,
status varchar(255) not null,
diet_for varchar(255) not null,
calories_to_be_burn varchar(255) not null,
calories_to_be_consume varchar(255) not null,
nutrition_id int,
foreign key (nutrition_id) references nutrition (nutrition_id)
); 

create table food_timings(
food_timing_id int auto_increment primary key,
food_time_title varchar(255) not null,
food_time varchar(255) not null,
calories_can_taken varchar(255) not null,
diet_id int,
foreign key (diet_id) references diet (diet_id)
); 

create table food_in_diet(
food_in_diet_id int auto_increment primary key,
food_name varchar(255) not null,
quantity varchar(255) not null,
units varchar(255) not null,
preparation_process varchar(255) not null,
propagation_time varchar(255) not null,
calories varchar(255) not null,
food_timing_id int,
image varchar(255) not null,
foreign key (food_timing_id) references food_timings (food_timing_id)
); 

create table exercise_timings(
exercise_timing_id int auto_increment primary key,
exercise_title varchar(255) not null,
exercise_time varchar(255) not null,
calories_should_burn  varchar(255) not null,
diet_id int,
foreign key (diet_id) references diet (diet_id)
); 

create table exercise_in_diet(
exercise_in_diet_id int auto_increment primary key,
exercise_name varchar(255) not null,
duration varchar(255) not null,
calories_burn varchar(255) not null,
exercise_timing_id int,
image varchar(255) not null,
foreign key (exercise_timing_id) references exercise_timings (exercise_timing_id)
);

create table user_diet(
user_diet_id int auto_increment primary key,
status varchar(255) not null,
user_id int,
diet_id int,
foreign key (diet_id) references diet (diet_id),
foreign key (user_id) references user (user_id)
); 

create table user_food(
user_food_id int auto_increment primary key,
quantity varchar(255) not null,
date varchar(255) not null,
user_diet_id int,
food_in_diet_id int,
totalCalories varchar(255),
foreign key (food_in_diet_id) references food_in_diet (food_in_diet_id),
foreign key (user_diet_id) references user_diet(user_diet_id)
); 

create table user_exercise(
user_exercise_id int auto_increment primary key,
number_of_sets varchar(255) not null,
date varchar(255) not null,
user_diet_id int,
exercise_in_diet_id int,
totalCalories varchar(255),
foreign key (exercise_in_diet_id) references exercise_in_diet (exercise_in_diet_id),
foreign key (user_diet_id) references user_diet (user_diet_id)

); 


create table discussion_on_diet(
discussion_on_diet_id int auto_increment primary key,
comment varchar(255) not null,
date_timing varchar(255) not null,
user_diet_id int,
foreign key (user_diet_id) references user_diet (user_diet_id)
  );
  
create table review(
review_id int auto_increment primary key,
review varchar(255) not null,
rating varchar(255) not null,
date varchar(255) not null,
user_diet_id int,
foreign key (user_diet_id) references user_diet (user_diet_id)
);

create table beforeNotify(
beforeNotifyId int auto_increment primary key,
user_id int,
status varchar(255),
food_timing_id int,
exercise_timing_id int,
foreign key (user_id) references user (user_id),
foreign key (food_timing_id) references food_timings (food_timing_id),
foreign key (exercise_timing_id) references exercise_timings (exercise_timing_id)

);





create table equalNotify(
equalNotifyId int auto_increment primary key,
user_id int,
status varchar(255),
food_timing_id int,
exercise_timing_id int,
foreign key (user_id) references user (user_id),
foreign key (food_timing_id) references food_timings (food_timing_id),
foreign key (exercise_timing_id) references exercise_timings (exercise_timing_id)
);


