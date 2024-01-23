% include("bootstrap.tpl")

<title>Driver List | Project D</title>

<style>
	.main-container {
		background: url("/static/images/page-driver-list/background.png");
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
	<div class="container min-vh-100 bg-light p-5" style="--bs-bg-opacity: .50">
		<!-- Page Header -->
		<header class="text-center pb-5">
			<p>&nbsp;</p>
			<h1 class="display-1">Driver List</h1>
			<p><a href="/">Back To Main Page</a></p>
			<p>&nbsp;</p>
		</header>

		<!-- Course Cards -->
		<div class="row g-4 pb-5">
			% for id, name, car, team_id, gender, img, team_name, win, draw, loss in drivers:
				% win  = 0 if win  == None else win
				% draw = 0 if draw == None else draw
				% loss = 0 if loss == None else loss
				% team_name = "Solo Driver" if team_name == None else team_name
				<div class="col-md-4 col-sm-6 col-xs-12">
					<a class="link-underline link-underline-opacity-0" href="/drivers/{{id}}">
						<div class="card shadow-sm">
							<div class="ratio ratio-1x1 card-img-top">
								<img src="/static/{{img}}" alt="{{name}} Driver Card" loading="lazy">
							</div>
							<div class="card-body text-center">
								<h5 class="card-title">{{name}}</h5>
								<p class="card-text">
									<span>{{team_name}}</span></br>
									<span>Drives a {{car}}</span></br>
									<span>{{win}} W / {{draw}} D / {{loss}} L</span>
								</p>
							</div>
						</div>
					</a>
				</div>
			% end
		</div>
	</div>
</div>
