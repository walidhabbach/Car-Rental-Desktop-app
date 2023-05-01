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

CREATE TABLE carburant (
  idCarburant   int not null AUTO_INCREMENT,
  nom VARCHAR(254),
  primary key (idCarburant)
);

/*==============================================================*/
/* Table : client                                               */
/*==============================================================*/
 CREATE TABLE client (
      idUser int(11),
      adresse varchar(254),
      cin varchar(50),
      photo LONGBLOB,
      liste_noire tinyint(1),
      permis varchar(20),
      passport varchar(20),
      email varchar(60),
      observation varchar(254),
      societe varchar(50),
      ville varchar(50),
      tel varchar(30),
      date_permis date
    );

/*==============================================================*/
/* Table : marque                                               */
/*==============================================================*/
CREATE TABLE marque (
    idMarque int PRIMARY KEY,
    logo LONGBLOB,
    nom VARCHAR(254)
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
CREATE TABLE utilisateur (
    idUser int(11),
    nom varchar(32),
    prenom varchar(32),
    login varchar(50),
    mdp varchar(50)
  );
/*==============================================================*/
/* Table : voiture                                              */
/*==============================================================*/
CREATE TABLE voiture (
  idCar INT(11) PRIMARY KEY AUTO_INCREMENT,
  idMarque INT(11),
  idCarburant INT(11),
  image LONGBLOB,
  model VARCHAR(255)
);


alter table client add constraint FK_client_utilisateur foreign key (idUser)
      references utilisateur (idUser) on delete CASACADE on update restrict;

ALTER TABLE reservation
ADD CONSTRAINT FK_reservation_client FOREIGN KEY (idUser)
REFERENCES client(idUser) ON DELETE CASCADE ON UPDATE RESTRICT,
ADD CONSTRAINT FK_reservation_voiture FOREIGN KEY (idCar)
REFERENCES voiture(idCar) ON DELETE CASCADE ON UPDATE RESTRICT;

alter table super_utilisateur add constraint FK_superuser_user foreign key (idUser)
      references utilisateur (idUser) on delete restrict on update restrict;

alter table voiture add constraint FK_voiture_carburant foreign key (idCarburant)
      references carburant (idCarburant) on delete restrict on update restrict;

alter table voiture add constraint FK_voiture_marque foreign key (idMarque)
      references marque (idMarque) on delete restrict on update restrict;

