/*==============================================================*/
/* Nom de SGBD :  MySQL 5.0                                     */
/* Date de création :  20/04/2023 14:10:36                      */
/*==============================================================*/


drop table if exists carburant;

drop table if exists client;

drop table if exists marque;

drop table if exists reservation;

drop table if exists super_utilisateur;

drop table if exists utilisateur;

drop table if exists voiture;

/*==============================================================*/
/* Table : carburant                                            */
/*==============================================================*/
create table carburant
(
   idCarburant          int not null AUTO_INCREMENT,
   nom                  int,
   primary key (idCarburant)
);

/*==============================================================*/
/* Table : client                                               */
/*==============================================================*/
create table client
(
   idUser               int not null ,
   adresse              varchar(254) not null,
   cin                  varchar(50) not null,
   photo                blob,
   primary key (idUser)
);

/*==============================================================*/
/* Table : marque                                               */
/*==============================================================*/
create table marque
(
   idMarque             int not null AUTO_INCREMENT,
   logo                 int,
   primary key (idMarque)
);

/*==============================================================*/
/* Table : reservation                                          */
/*==============================================================*/
create table reservation
(
   idCar                int,
   idUser               int,
   date_res             varchar(254)
);

/*==============================================================*/
/* Table : super_utilisateur                                    */
/*==============================================================*/
create table super_utilisateur
(
   idUser               int not null,
   admin                bool,
   primary key (idUser)
);

/*==============================================================*/
/* Table : utilisateur                                          */
/*==============================================================*/
create table utilisateur
(
   idUser               int not null AUTO_INCREMENT,
   nom                  varchar(32) not null,
   prenom               varchar(32) not null,
   primary key (idUser)
);

/*==============================================================*/
/* Table : voiture                                              */
/*==============================================================*/
create table voiture
(
   idCar                int not null AUTO_INCREMENT,
   idMarque             int,
   idCarburant          int,
   image                int,
   primary key (idCar)
);

alter table client add constraint FK_client_utilisateur foreign key (idUser)
      references utilisateur (idUser) on delete restrict on update restrict;

ALTER TABLE reservation
ADD CONSTRAINT FK_reservation_client FOREIGN KEY (idUser)
REFERENCES client(idUser) ON DELETE RESTRICT ON UPDATE RESTRICT,
ADD CONSTRAINT FK_reservation_voiture FOREIGN KEY (idCar)
REFERENCES voiture(idCar) ON DELETE RESTRICT ON UPDATE RESTRICT;

alter table super_utilisateur add constraint FK_superuser_user foreign key (idUser)
      references utilisateur (idUser) on delete restrict on update restrict;

alter table voiture add constraint FK_voiture_carburant foreign key (idCarburant)
      references carburant (idCarburant) on delete restrict on update restrict;

alter table voiture add constraint FK_voiture_marque foreign key (idMarque)
      references marque (idMarque) on delete restrict on update restrict;

