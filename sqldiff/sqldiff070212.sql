BEGIN;
ALTER TABLE "mumbai_area"
	ADD "display_name" text;
ALTER TABLE "mumbai_area"
	ADD "slug" varchar(50);
CREATE INDEX "mumbai_area_slug_idx"
	ON "mumbai_area" ("slug");
-- Comment: Unknown database type for field 'geometry' (16394)
-- Model: Road
ALTER TABLE "mumbai_road"
	ADD "display_name" text;
ALTER TABLE "mumbai_road"
	ADD "slug" varchar(50);
CREATE INDEX "mumbai_road_slug_idx"
	ON "mumbai_road" ("slug");
-- Comment: Unknown database type for field 'geometry' (16394)
-- Model: Stop
ALTER TABLE "mumbai_stop"
	ADD "display_name" text;
ALTER TABLE "mumbai_stop"
	ADD "slug" varchar(50);
CREATE INDEX "mumbai_stop_slug_idx"
	ON "mumbai_stop" ("slug");
-- Comment: Unknown database type for field 'point' (16394)
-- Model: Route
ALTER TABLE "mumbai_route"
	ADD "slug" varchar(50);
CREATE INDEX "mumbai_route_slug_idx"
	ON "mumbai_route" ("slug");
-- Model: RouteDetail
--ALTER TABLE "mumbai_routedetail"
--	ADD "route_code" text;
-- Model: Landmark
ALTER TABLE "mumbai_landmark"
	ADD "display_name" text;
ALTER TABLE "mumbai_landmark"
	ADD "slug" varchar(50);
CREATE INDEX "mumbai_landmark_slug_idx"
	ON "mumbai_landmark" ("slug");
-- Comment: Unknown database type for field 'point' (16394)
-- Model: StopLocation
-- Comment: Unknown database type for field 'point' (16394)
COMMIT;
