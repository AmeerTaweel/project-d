% include("bootstrap.tpl")

% id, did, cid, date, min, bid, dname, cname = record

<title>Record #{{id}} | Project D</title>

<style>
	.main-container {
		background: url("/static/images/page-record-info/background.png");
		background-repeat: no-repeat;
		background-size: cover;
		backdrop-filter: blur(5px);
		background-position: center;
		background-attachment: fixed;
		position: fixed;
	}

	.blur {
		background: rgba(255, 255, 255, 0.25);
		backdrop-filter: blur(5px);
		background-position: center;
		background-attachment: fixed;
		position: fixed;
		overflow-y: scroll;
	}
</style>

<div class="main-container container-fluid h-100 p-0">
	<div class="blur w-100 h-100"/>
	<div class="container min-vh-100 bg-light ps-5 pe-5" style="--bs-bg-opacity: .50">
		<!-- Main Page Header -->
		<header class="text-center p-5">
			<p>&nbsp;</p>
			<h1 class="display-1">Record #{{id}}</h1>
			<p><a href="/records">Back To Records Page</a></p>
			<p>&nbsp;</p>
		</header>

		<!-- Info Cards -->
		<div class="row g-4">
			<div class="col-md-4 col-sm-6 col-xs-12">
				<a class="link-underline link-underline-opacity-0" href="/drivers/{{did}}">
					<div class="card shadow-sm">
						<div class="card-body">
							<h5 class="card-title text-center">Driver</h5>
							<h5 class="card-title text-center">{{dname}}</h5>
						</div>
					</div>
				</a>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				<a class="link-underline link-underline-opacity-0" href="/courses/{{cid}}">
					<div class="card shadow-sm">
						<div class="card-body">
							<h5 class="card-title text-center">Course</h5>
							<h5 class="card-title text-center">{{cname}}</h5>
						</div>
					</div>
				</a>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				<div class="card shadow-sm">
					<div class="card-body">
						<h5 class="card-title text-center">Date</h5>
						<h5 class="card-title text-center">{{date}}</h5>
					</div>
				</div>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				<div class="card shadow-sm">
					<div class="card-body">
						<h5 class="card-title text-center">Minutes</h5>
						<h5 class="card-title text-center">{{round(min, 3)}}</h5>
					</div>
				</div>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				% if bid != None:
					<a class="link-underline link-underline-opacity-0" href="/battles/{{bid}}">
						<div class="card shadow-sm">
							<div class="card-body">
								<h5 class="card-title text-center">Battle</h5>
								<h5 class="card-title text-center">{{bid}}</h5>
							</div>
						</div>
					</a>
				% else:
					<div class="card shadow-sm">
						<div class="card-body">
							<h5 class="card-title text-center">Battle</h5>
							<h5 class="card-title text-center">N/A</h5>
						</div>
					</div>
				% end
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				% if team_battle_id != None:
					<a class="link-underline link-underline-opacity-0" href="/team-battles/{{team_battle_id}}">
						<div class="card shadow-sm">
							<div class="card-body">
								<h5 class="card-title text-center">Team Battle</h5>
								<h5 class="card-title text-center">{{team_battle_id}}</h5>
							</div>
						</div>
					</a>
				% else:
					<div class="card shadow-sm">
						<div class="card-body">
							<h5 class="card-title text-center">Team Battle</h5>
							<h5 class="card-title text-center">N/A</h5>
						</div>
					</div>
				% end
			</div>
		</div>
	</div>
</div>
