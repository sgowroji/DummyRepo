
module.exports = async ({ github, context }) => {

    let issues = await github.rest.issues.listForRepo({
        owner: context.repo.owner,
        repo: context.repo.repo,
        state: "open",
        labels: "p0"
    });

    
    if (issues.status != 200)
        return

   let issueList = issues.data
    console.log("issue list")
    for (let i = 0; i < issueList.length; i++) {

        let number = issueList[i].number;
        let resp = await github.rest.issues.listEventsForTimeline({
            owner: context.repo.owner,
            repo: context.repo.repo,
            issue_number: number,
        });
        let events = resp.data;
        console.log("event")
        for (let i = 0; i < events.length; i++) {
            let event_details = events[i];
            console.log("event_details",event_details)
            if (event_details.event == 'labeled' && event_details.label && event_details.label.name == "p0") {
                let currentDate = new Date();
                let labeledDate = new Date(event_details.created_at)
                console.log("time diff",currentDate - labeledDate)
                if (currentDate - labeledDate >= 0) {
                    await github.rest.issues.removeLabel({
                        issue_number: number,
                        owner: context.repo.owner,
                        repo: context.repo.repo,
                        name: "p0"

                    })

                    await github.rest.issues.addLabels({
                        issue_number: number,
                        owner: context.repo.owner,
                        repo: context.repo.repo,
                        labels:["p1"]

                    })
                }

            }
        }
    }
}
