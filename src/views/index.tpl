% include("bootstrap.tpl")

<title>Project D</title>

<style>
	.main-container {
		background: url("/static/images/page-index/background.png");
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
			<p>COMP306 Final Project</p>
			<h1 class="display-1">Project D</h1>
			<p>Future Gadget Lab</p>
			<p>Ameer Taweel, Ahmed Jareer, Omar Asaad</p>
		</header>

		<!-- Python Code Block -->
		<%
			pages = (
				("Courses"           , "courses"),
				("Teams  "           , "teams"),
				("Drivers"           , "drivers"),
				("Records"           , "records"),
				("Individual Battles", "battles"),
				("Team Battles"      , "team-battles")
			)
		%>

		<!-- Navigation Cards -->
		<div class="row g-4">
			% for name, id in pages:
				<div class="col-md-4 col-sm-6 col-xs-12">
					<a class="link-underline link-underline-opacity-0" href="/{{id}}">
						<div class="card shadow-sm">
							<img src="/static/images/page-index/page-{{id}}.png" class="card-img-top" alt="{{name}} Page Card">
							<div class="card-body">
								<h5 class="card-title text-center">{{name}}</h5>
							</div>
						</div>
					</a>
				</div>
			% end
		</div>
	</div>
</div>
