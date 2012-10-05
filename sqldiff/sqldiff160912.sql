


ALTER TABLE "mumbai_route" ADD COLUMN "code3" varchar(5) NOT NULL;

ALTER TABLE "mumbai_route" ADD COLUMN "route_type_id" integer;

ALTER TABLE "mumbai_route" ADD CONSTRAINT "route_type_id_refs_id_6b818b01" FOREIGN KEY ("route_type_id") REFERENCES "mumbai_routetype" ("id") DEFERRABLE INITIALLY DEFERRED;
