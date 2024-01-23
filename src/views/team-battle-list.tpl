% include("bootstrap.tpl")

<title>Team Battle List | Project D</title>

<style>
	.main-container {
		background: url("/static/images/page-team-battle-list/background.png");
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
			<h1 class="display-1">Team Battle List</h1>
			<p><a href="/">Back To Main Page</a></p>
			<p>&nbsp;</p>
		</header>

		<table class="table">
			<thead>
				<tr>
					<th scope="col">Team Battle</th>
					<th scope="col">Winner</th>
					<th scope="col">Loser</th>
					<th scope="col">Course</th>
					<th scope="col">Date</th>
				</tr>
			</thead>
			<tbody>
				% for tbid, date, tid1, tname1, tid2, tname2, cid, cname, points1, points2 in battles:
					<tr style="white-space: nowrap">
						<td><a href="/team-battles/{{tbid}}">{{tbid}}</a></td>
						% if points1 > points2:
							<td><a href="/teams/{{tid1}}" class="text-truncate">{{tname1}}</a></td>
							<td><a href="/teams/{{tid2}}" class="text-truncate">{{tname2}}</a></td>
						% else:
							<td><a href="/teams/{{tid2}}" class="text-truncate">{{tname2}}</a></td>
							<td><a href="/teams/{{tid1}}" class="text-truncate">{{tname1}}</a></td>
						% end
						<td><a href="/courses/{{cid}}" class="text-truncate">{{cname}}</a></td>
						<td>{{date}}</td>
					</tr>
				% end
			</tbody>
		</table>
	</div>
</div>
