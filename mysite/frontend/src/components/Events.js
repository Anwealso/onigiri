import React, { Component } from "react";
import { Grid, Button, Typography, Card, CardContent, CardActions, CardMedia} from "@material-ui/core";
import Navbar from "./Navbar";
import UserInfo from "./UserInfo";
import { Link } from 'react-router-dom';

export default class Events extends Component {
  constructor(props) {
    super(props);

    this.state = {
      events: [],
      user: UserInfo()
    };

    this.getPosts = this.getPosts.bind(this);
    this.getPosts();
    this.checkAttendance = this.checkAttendance.bind(this);
    // this.getPosts = this..bind(this);
  }

  componentDidMount() {
    this.timer = setInterval(()=> this.getPosts(), 100000);
  }
  
  componentWillUnmount() {
    clearInterval(this.timer) 
    this.timer = null;
  }

  checkAttendance(event_id) {
    if (this.state.user === null) {
      return "contained"
    }

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user: this.state.user.user_id,
        event: event_id,
      }),
    };
    fetch("/api/check-attendance", requestOptions)
      .then((response) => {
        console.log(response)
        return response.json()
      }).then((data) => {
        if (data.message == 1) {
          return "outlined" 
        } else {
          return "contained"
        }
      })
  }

  subscribeToEvent(event_id) {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user: this.state.user.user_id,
        event: event_id,
      }),
    };
    fetch("/api/submit-attendance", requestOptions)
      .then((response) => {
        console.log(response)

        if (response.ok) {
          console.log("Subscribed")
        } else {
          this.setState({ error: "Survey not found." });
        }
        return response.json()
      })
      .catch((error) => {
        console.log(error);
      });
  }

  renderMedia(props) {
    return (
      <div style={{ maxWidth: "600px" }}>
      <Card>
        <CardMedia
          component="img"
          height="250"
          image={props.image}
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {props.title}
          </Typography>
          <Typography variant="body2">
            {console.log(props.location)}
          At {props.location.substring(props.location.indexOf("!2s") + 3, props.location.indexOf("!5e0")).replaceAll("%2C%20", ", ").replaceAll("%20", " ").replaceAll("&#39;", "'").replaceAll("%26", "&")}, {props.time.substring(8,10)}/{props.time.substring(5,7)}
          </Typography>
          <Typography variant="body2">
            {props.description}
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="small" variant={this.checkAttendance(props.id)} onClick={() => { this.subscribeToEvent(props.id); }}>Subscribe</Button>
          <Link to={"/together/event/" + props.id}>
            <Button size="small">Learn More</Button>
          </Link>
        </CardActions>
      </Card>
      </div>
    );
  }

  // Feth from api and save to events array from state
  getPosts() {
    return fetch("/api/events")
      .then((response) => {
        console.log(response)
        if (!response.ok) {
          console.log("Response not okay")
          this.props.history.push("/");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Retrieved data from API")
        console.log(data)
        this.setState({
          events: data
        });
      });
  }


  render() {
    return (

      <Grid container spacing={1}>
          <Navbar />

          <Grid item xs={12} align="center">

                {this.state.events.map((event) => {
                    return (      
                      <Grid key={event.id} style={{backgroundColor: "ghostwhite", borderRadius: "20px", margin: "10px", padding: "10px", maxwidth: "500px"}}>
                        {this.renderMedia(event)}
                       </Grid>
                    );
                 })}
          </Grid>
        </Grid>
      );
  }
}
