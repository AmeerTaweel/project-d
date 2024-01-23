% include("bootstrap.tpl")

% id, name, loc, logo = team
% w, l = wl

<title>{{name}} | Team | Project D</title>

<style>
	.main-container {
		background: url("/static/{{logo}}");
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
			<h1 class="display-1">Team Info: {{name}}</h1>
			<p><a href="/teams">Back To Teams Page</a></p>
			<p>&nbsp;</p>
		</header>

		<div class="row g-4 pb-5">
			<div class="col-md-4 col-sm-6 col-xs-12">
				<p class="ratio ratio-1x1 card-img-top">
					<img src="/static/{{logo}}" alt="{{name}} Team Logo">
				</p>
				<p class="h3">Location: {{loc}}</p>
				<p class="h3">{{w}} W / {{l}} L</p>
			</div>
			<div class="col-md-8 col-sm-6 col-xs-12">
				<%
					tabs = (
						("Members"               , "members"),
						("Team Battles"          , "battles"),
						("Performance Per Course", "per-course"),
						("Performance Per Team"  , "per-team")
					)
				%>
				<ul class="nav nav-tabs nav-fill pb-3">
					% for i, tab in enumerate(tabs):
						% tab_name, tab_id = tab
						% active = "active" if i == 0 else ""
						<li class="nav-item">
							<button class="nav-link {{active}}" id="{{tab_id}}-tab"
							data-bs-toggle="tab" data-bs-target="#{{tab_id}}-pane"
							type="button">
								{{tab_name}}
							</button>
						</li>
					% end
				</ul>
				<div class="tab-content">
					<div class="tab-pane fade show active" id="members-pane">
						<table class="table">
							<thead>
								<tr>
									<th scope="col">Name</th>
									<th scope="col">Car</th>
									<th scope="col">Gender</th>
								</tr>
							</thead>
							<tbody>
								% for did, dname, dcar, dteamid, dgender, dimg in members:
									<tr style="white-space: nowrap">
										<td><a href="/drivers/{{did}}" class="text-truncate">{{dname}}</a></td>
										<td>{{dcar}}</td>
										<td>{{dgender}}</td>
									</tr>
								% end
							</tbody>
						</table>
					</div>
					<div class="tab-pane fade" id="battles-pane">
						<table class="table">
							<thead>
								<tr>
									<th scope="col">Team Battle</th>
									<th scope="col">Against</th>
									<th scope="col">Result</th>
									<th scope="col">Date</th>
								</tr>
							</thead>
							<tbody>
								% for tbid, tid, tname, date, points1, points2 in all_team_battles:
									<tr style="white-space: nowrap">
										<td><a href="/team-battles/{{tbid}}">{{tbid}}</a></td>
										<td><a href="/teams/{{tid}}" class="text-truncate">{{tname}}</a></td>
										% if points1 > points2:
											<td>Win</td>
										% else:
											<td>Loss</td>
										% end
										<td>{{date}}</td>
									</tr>
								% end
							</tbody>
						</table>
					</div>
					<div class="tab-pane fade" id="per-course-pane">
						<table class="table">
							<thead>
								<tr>
									<th scope="col">Course</th>
									<th scope="col">Wins</th>
									<th scope="col">Losses</th>
								</tr>
							</thead>
							<tbody>
								% for cid, cname, w, l in wl_per_course:
									<tr style="white-space: nowrap">
										<td><a href="/courses/{{cid}}" class="text-truncate">{{cname}}</a></td>
										<td>{{w}}</td>
										<td>{{l}}</td>
									</tr>
								% end
							</tbody>
						</table>
					</div>
					<div class="tab-pane fade" id="per-team-pane">
						<table class="table">
							<thead>
								<tr>
									<th scope="col">Team</th>
									<th scope="col">Wins</th>
									<th scope="col">Losses</th>
								</tr>
							</thead>
							<tbody>
								% for tid, tname, w, l in wl_per_course:
									<tr style="white-space: nowrap">
										<td><a href="/teams/{{tid}}" class="text-truncate">{{tname}}</a></td>
										<td>{{w}}</td>
										<td>{{l}}</td>
									</tr>
								% end
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
