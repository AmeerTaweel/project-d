% include("bootstrap.tpl")

% rid1, did1, cid, date, min1, bid, rid2, did2, _, _, min2, _, dname1, dname2, cname, tbid = battle

<title>Battle #{{bid}} | Project D</title>

<style>
	.main-container {
		background: url("/static/images/page-battle-info/background.png");
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
			<h1 class="display-1">Battle #{{bid}}</h1>
			<p><a href="/battles">Back To Battles Page</a></p>
			<p>&nbsp;</p>
		</header>

		<!-- Info Cards -->
		<div class="row g-4">
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
						<h5 class="card-title text-center">Result</h5>
						% if min1 < min2:
							<h5 class="card-title text-center">Win For 1</h5>
						% elif min1 > min2:
							<h5 class="card-title text-center">Win For 2</h5>
						% else:
							<h5 class="card-title text-center">Draw</h5>
						% end
					</div>
				</div>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				<a class="link-underline link-underline-opacity-0" href="/records/{{rid1}}">
					<div class="card shadow-sm">
						<div class="card-body">
							<h5 class="card-title text-center">Record 1</h5>
							<h5 class="card-title text-center">#{{rid1}}</h5>
						</div>
					</div>
				</a>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				<a class="link-underline link-underline-opacity-0" href="/drivers/{{did1}}">
					<div class="card shadow-sm">
						<div class="card-body">
							<h5 class="card-title text-center">Driver 1</h5>
							<h5 class="card-title text-center">{{dname1}}</h5>
						</div>
					</div>
				</a>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				<div class="card shadow-sm">
					<div class="card-body">
						<h5 class="card-title text-center">Minutes 1</h5>
						<h5 class="card-title text-center">{{round(min1, 3)}}</h5>
					</div>
				</div>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				<a class="link-underline link-underline-opacity-0" href="/records/{{rid2}}">
					<div class="card shadow-sm">
						<div class="card-body">
							<h5 class="card-title text-center">Record 2</h5>
							<h5 class="card-title text-center">#{{rid2}}</h5>
						</div>
					</div>
				</a>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				<a class="link-underline link-underline-opacity-0" href="/drivers/{{did2}}">
					<div class="card shadow-sm">
						<div class="card-body">
							<h5 class="card-title text-center">Driver 2</h5>
							<h5 class="card-title text-center">{{dname2}}</h5>
						</div>
					</div>
				</a>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				<div class="card shadow-sm">
					<div class="card-body">
						<h5 class="card-title text-center">Minutes 2</h5>
						<h5 class="card-title text-center">{{round(min2, 3)}}</h5>
					</div>
				</div>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				% if tbid != None:
					<a class="link-underline link-underline-opacity-0" href="/team-battles/{{tbid}}">
						<div class="card shadow-sm">
							<div class="card-body">
								<h5 class="card-title text-center">Team Battle</h5>
								<h5 class="card-title text-center">{{tbid}}</h5>
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
