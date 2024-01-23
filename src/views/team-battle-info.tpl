% include("bootstrap.tpl")

% tbid, _, _, _, cid, cname, date, tid1, tname1, tid2, tname2, _, _, _, _ = battles[0]

<title>Team Battle {{tbid}} | Project D</title>

<style>
	.main-container {
		background: url("/static/images/page-team-battle-info/background.png");
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
			<h1 class="display-1">Team Battle #{{tbid}}</h1>
			<p><a href="/team-battles">Back To Team Battles Page</a></p>
			<p>&nbsp;</p>
		</header>

		<%
			score1 = 0
			score2 = 0
			for battle in battles:
				min1, min2 = battle[2], battle[3]
				score1 += 1 if min2 > min1 else 0
				score2 += 1 if min2 < min1 else 0
			end
		%>
		<div class="row g-4">
			<div class="col-md-4 col-sm-6 col-xs-12">
				<a class="link-underline link-underline-opacity-0" href="/teams/{{tid1}}">
					<div class="card shadow-sm">
						<div class="card-body">
							<h5 class="card-title text-center">Team 1</h5>
							<h5 class="card-title text-center">{{tname1}}</h5>
						</div>
					</div>
				</a>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				<a class="link-underline link-underline-opacity-0" href="/teams/{{tid2}}">
					<div class="card shadow-sm">
						<div class="card-body">
							<h5 class="card-title text-center">Team 2</h5>
							<h5 class="card-title text-center">{{tname2}}</h5>
						</div>
					</div>
				</a>
			</div>
			<div class="col-md-4 col-sm-6 col-xs-12">
				<div class="card shadow-sm">
					<div class="card-body">
						<h5 class="card-title text-center">Score</h5>
						<h5 class="card-title text-center">{{score1}}-{{score2}}</h5>
					</div>
				</div>
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
			<div class="col-md-4 col-sm-6 col-xs-12 pb-5">
				% if score1 > score2:
					<a class="link-underline link-underline-opacity-0" href="/teams/{{tid1}}">
						<div class="card shadow-sm">
							<div class="card-body">
								<h5 class="card-title text-center">Winner</h5>
								<h5 class="card-title text-center">{{tname1}}</h5>
							</div>
						</div>
					</a>
				% else:
					<a class="link-underline link-underline-opacity-0" href="/teams/{{tid2}}">
						<div class="card shadow-sm">
							<div class="card-body">
								<h5 class="card-title text-center">Winner</h5>
								<h5 class="card-title text-center">{{tname2}}</h5>
							</div>
						</div>
					</a>
				% end
			</div>
		</div>

		<table class="table">
			<thead>
				<tr>
					<th scope="col">Battle</th>
					<th scope="col">Driver 1</th>
					<th scope="col">Driver 2</th>
					<th scope="col">Minutes 1</th>
					<th scope="col">Minutes 2</th>
					<th scope="col">Result</th>
				</tr>
			</thead>
			<tbody>
				% for _, bid, min1, min2, _, _, _, _, _, _, _, did1, dname1, did2, dname2 in battles:
					<tr style="white-space: nowrap">
						<td><a href="/battles/{{bid}}">{{bid}}</a></td>
						<td><a href="/drivers/{{did1}}" class="text-truncate">{{dname1}}</a></td>
						<td><a href="/drivers/{{did2}}" class="text-truncate">{{dname2}}</a></td>
						<td>{{round(min1, 3)}}</td>
						<td>{{round(min2, 3)}}</td>
						% if min1 == min2:
							<td>Draw</td>
						% elif min1 < min2:
							<td>Win For 1</td>
						% else:
							<td>Win For 2</td>
						% end
					</tr>
				% end
			</tbody>
		</table>
	</div>
</div>
