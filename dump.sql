create schema raffle collate latin1_swedish_ci;

create table users
(
	id int auto_increment,
	role varchar(50) null,
	first_name varchar(20) null,
	last_name varchar(30) null,
	address varchar(35) null,
	city varchar(30) null,
	state varchar(25) null,
	zip varchar(10) null,
	phone varchar(25) null,
	email varchar(50) null,
	password varchar(255) null,
	active tinyint(1) null,
	comments varchar(500) null,
	created_at datetime null,
	updated_at datetime null,
	constraint users_id_uindex
		unique (id)
);

alter table users
	add primary key (id);

create table items
(
	id int auto_increment,
	name varchar(45) null,
	description varchar(250) null,
	price float null,
	available tinyint(1) null,
	category varchar(255) null,
	created_by int null,
	created_at datetime null,
	updated_at datetime null,
	constraint items_id_uindex
		unique (id),
	constraint items_users_id_fk
		foreign key (created_by) references users (id)
);

alter table items
	add primary key (id);

create table item_images
(
	id int auto_increment,
	item_id int null,
	path varchar(255) null,
	created_by int null,
	created_at datetime null,
	updated_at datetime null,
	constraint item_images_id_uindex
		unique (id),
	constraint item_images_items_id_fk
		foreign key (item_id) references items (id),
	constraint item_images_users_id_fk
		foreign key (created_by) references users (id)
);

alter table item_images
	add primary key (id);

create table orders
(
	id int auto_increment,
	user_id int null,
	square_checkout_id varchar(50) null,
	square_order_id varchar(50) null,
	square_reference_id varchar(50) null,
	square_transaction_id varchar(50) null,
	payment_status varchar(50) null,
	order_total float null,
	created_at datetime null,
	updated_at datetime null,
	constraint orders_id_uindex
		unique (id),
	constraint orders_users_id_fk
		foreign key (user_id) references users (id)
);

alter table orders
	add primary key (id);

create table tickets
(
	id int auto_increment,
	user_id int null,
	item_id int null,
	order_id int null,
	active tinyint(1) null,
	is_winner tinyint(1),
	created_at datetime null,
	updated_at datetime null,
	constraint tickets_id_uindex
		unique (id),
	constraint tickets_items_id_fk
		foreign key (item_id) references items (id),
	constraint tickets_orders_id_fk
		foreign key (order_id) references orders (id),
	constraint tickets_users_id_fk
		foreign key (user_id) references users (id)
);

alter table tickets
	add primary key (id);

