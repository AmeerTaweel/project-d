% include("bootstrap.tpl")

<title>Team List | Project D</title>

<style>
	.main-container {
		background: url("/static/images/page-team-list/background.png");
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
			<h1 class="display-1">Team List</h1>
			<p><a href="/">Back To Main Page</a></p>
			<p>&nbsp;</p>
		</header>

		<!-- Team Cards -->
		<div class="row g-4 pb-5">
			% for id, name, loc, logo, win, loss, members in teams:
				<div class="col-md-4 col-sm-6 col-xs-12">
					<a class="link-underline link-underline-opacity-0" href="/teams/{{id}}">
						<div class="card shadow-sm">
							<div class="ratio ratio-1x1 card-img-top">
								<img src="/static/{{logo}}" alt="{{name}} Team Card" loading="lazy">
							</div>
							<div class="card-body text-center">
								<h5 class="card-title">{{name}}</h5>
								<p class="card-text">
									<span>{{loc}}</span></br>
									% if members == 1:
										<span>1 Member</span></br>
									% else:
										<span>{{members}} Members</span></br>
									% end
									<span>{{win}} W / {{loss}} L</span>
								</p>
							</div>
						</div>
					</a>
				</div>
			% end
		</div>
	</div>
</div>
