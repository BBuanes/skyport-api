package skyport.api.game;

import com.google.gson.annotations.SerializedName;

public enum Direction {
    up,
    down,
    @SerializedName("right-up")
    rightUp,
    @SerializedName("right-down")
    rightDown,
    @SerializedName("left-up")
    leftUp,
    @SerializedName("left-down")
    leftDown
}
