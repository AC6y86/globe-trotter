# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/add-spatial-sdk-to-app.md
---
title: Add Spatial SDK to an existing 2D app
description: This tutorial will give you hands-on practice adding Spatial SDK to an existing 2D Android app using Meta Spatial Editor and Meta Spatial SDK.
last_updated: 2025-03-17
---

By the end of this tutorial, you'll have used Spatial SDK to add a 3D virtual environment to an existing 2D Android app, where the app will appear as an interactable panel. For your first time through this tutorial, we recommend using the template app provided below since its file structure matches the instructions exactly. However, you can also follow these steps using your own Android app.

If you'd rather make a Spatial SDK app from scratch, see [Create a new Spatial SDK app](/documentation/spatial-sdk/create-new-spatial-sdk-app/).

## Download and open the template Android app

Before you add a 3D environment, you'll preview the app as a regular 2D phone app.

1. Download or clone the [MediaSpatialAppTemplate GitHub repository](https://github.com/fbsamples/MediaSpatialAppTemplate), which is a template Android phone app.

2. If you downloaded the template app, unzip it. If you cloned the app, the folder is already unzipped.

3. In Android Studio, select **File** > **Open**.

    The **Open File or Project** window appears.

4. In the **Open File or Project** window, expand the unzipped folder, and then double-click **MediaSpatialAppTemplate-main**.

4. If Android Studio prompts you to upgrade and sync Gradle, upgrade it to the recommended version. This may take a while.

5. In the top toolbar, in the device dropdown to the left of the green **Run 'app'** button, set the Android emulator to **Medium Phone API 35** or any other phone emulator.

6. Click the green play button (the **Run 'app'** button).

    Here's what you should see in the Android Studio emulator.

    ![Screenshot of the emulator running the sample app](/images/fa_aether_tutorial_start_1.png)

    _"(c) copyright 2008, Blender Foundation, www.blender.org"_

7. In Android Studio, click the red **Stop** button to stop the app.

## Add a Meta Quest build variant

To add Spatial SDK to the template app, you are going to create a new [build variant](https://developer.android.com/build/build-variants). A build variant lets you have a mobile version of your app (for phones) and a Quest version (for Meta Quest devices) in the same codebase.

**Note**: The sample app doesn't use Groovy.  If you're following this tutorial using your own app and it uses Groovy (`build.gradle` instead of `build.gradle.kts`), read the [build variant](https://developer.android.com/build/build-variants#product-flavors) page for Groovy syntax.

1. On the left side of Android Studio, click the folder icon to open the project directory.

    The project directory panel appears.

2. At the top of the panel, ensure the file view setting is set to **Project Files** and not **Android**. This ensures your project directory layout matches the screenshots in this tutorial.

3. Open `app/build.gradle.kts`. This file is different from just `build.gradle.kts`, which isn't in the **app** folder.

4. Add this code just before the end of the `android` block. It specifies two build types, one for mobile, and one for Quest.

    ```kotlin
    buildFeatures { buildConfig = true }
    flavorDimensions += "device"
    productFlavors {
      create("mobile") { dimension = "device" }
      create("quest") { dimension = "device" }
      }
    ```

5. Save the file.

6. In the project directory, copy  `app/src/main/AndroidManifest.xml` to the `src/mobile` and `src/quest` folders.

    You'll see this error `Unresolved class 'MainActivity'`, but that's expected.

7. Sync the project with Gradle by clicking the **Sync Project with Gradle Files** button (the elephant icon) in the toolbar.

    ![GIF of the Gradle sync icon being clicked](/images/fa_aether_tutorial_start_syncgradle.gif)

8. In the top toolbar, select **Build** > **Select Build Variant**.

    The **Build Variants** panel appears on the left.

9. In the **Build Variants** panel, click **mobileDebug (default)**.

    A dropdown appears.

10. From the dropdown, select **questDebug** as the active build variant.

    Here's a video showing the change:

    <section>
      <embed-video width="100%">
        <video-source handle="GBmTUwJ4LAKMUu4FAFNEXcBscyAobosWAAAF" />
      </embed-video>
    </section>

    Now your app will use `src/quest/AndroidManifest.xml` when building. If you switch the build variant back to one of the mobile flavors, then your app will use `src/mobile/AndroidManifest.xml`.

## Add Spatial SDK Gradle plugin and dependencies

Spatial SDK is deployed to [Maven Central](https://central.sonatype.com/artifact/com.meta.spatial/meta-spatial-sdk) so it can be added to your app. In this step, you will add it to your project by editing your project level `build.gradle.kts` file and `app/build.gradle.kts` file to include the necessary dependencies.

**Note**: If you're using your own Android app for this tutorial instead of the sample app, your project structure is different. Follow [Setup the Spatial SDK Gradle plugin](/documentation/spatial-sdk/spatial-editor-using-with-sdk) instead of this section.

**Note**: The sample app doesn't use Groovy. If you're following this tutorial using your own app and it uses Groovy (`build.gradle` instead of `build.gradle.kts`), read the [build dependencies](https://developer.android.com/build/dependencies#add-dependency) page for Groovy syntax.

1. In your project level `build.gradle.kts` file (**not**  `app/build.gradle.kts`), replace the `plugins` block with this code.

    **Note**: If you choose to upgrade either the "org.jetbrains.kotlin.android" or "com.google.devtools.ksp" package versions at a later point, they must use the same version (ex. 2.0.20). Otherwise you'll get an error.

    ```kotlin
    plugins {
      id("com.android.application") version "8.1.0" apply false
      id("org.jetbrains.kotlin.android") version "2.0.20" apply false
      id("com.meta.spatial.plugin") version "0.6.0" apply (true)
      id("com.google.devtools.ksp") version "2.0.20-1.0.24" apply true
    }
    ```

2. Save the file.

3. In `app/build.gradle.kts`, replace the `plugins` block with this code.

    ```kotlin
    plugins {
        id("com.android.application")
        id("org.jetbrains.kotlin.android")
        id("com.google.devtools.ksp")
        id("com.meta.spatial.plugin")
    }
    ```

4. On the line before the `dependencies` block, add this code to create a variable for the Spatial SDK version.

    ```kotlin
    val metaSpatialSdkVersion = "0.6.0"
    ```

5. At the end of the `dependencies` block, add this code to import the relevant SDK packages.

    ```kotlin
    implementation("com.meta.spatial:meta-spatial-sdk:$metaSpatialSdkVersion")
    implementation("com.meta.spatial:meta-spatial-sdk-toolkit:$metaSpatialSdkVersion")
    implementation("com.meta.spatial:meta-spatial-sdk-vr:$metaSpatialSdkVersion")
      implementation("com.meta.spatial:meta-spatial-sdk-physics:$metaSpatialSdkVersion")
    ksp("com.meta.spatial.plugin:com.meta.spatial.plugin.gradle.plugin:0.6.0")
    ```

    You'll get a reference warning about **ksp**, but that's okay. You'll fix it by syncing with Gradle later in this section.

    There are other packages available besides the three listed above. For more information on all of the available Spatial SDK packages, see [Spatial SDK Packages](/documentation/spatial-sdk/spatial-sdk-packages).

    The variable declaration and `dependencies` block should now look like this.

    ```kotlin
    val metaSpatialSdkVersion = "0.6.0"

    dependencies {
    ...

    implementation("com.meta.spatial:meta-spatial-sdk:$metaSpatialSdkVersion")
    implementation("com.meta.spatial:meta-spatial-sdk-toolkit:$metaSpatialSdkVersion")
    implementation("com.meta.spatial:meta-spatial-sdk-vr:$metaSpatialSdkVersion")
      implementation("com.meta.spatial:meta-spatial-sdk-physics:$metaSpatialSdkVersion")
    ksp("com.meta.spatial.plugin:com.meta.spatial.plugin.gradle.plugin:0.6.0")
    }
    ```

5. Below the `dependencies` block, add this code to tell your Spatial SDK project where the Spatial Editor files are stored and enable custom components in Spatial Editor.

    You'll get a reference warning about this code, but that's okay. You'll fix it by syncing with Gradle in the next step.

    ```kotlin
    val projectDir = layout.projectDirectory
    val sceneDirectory = projectDir.dir("spatial_editor/MediaApp")
    spatial {
      allowUsageDataCollection = true
      scenes {
        exportItems {
          item {
            projectPath.set(sceneDirectory.file("Main.metaspatial"))
            outputPath.set(projectDir.dir("src/quest/assets/scenes"))
          }
        }
      }
    }

    afterEvaluate {
      tasks.named("assembleQuestDebug") {
        dependsOn("export")
        //finalizedBy("generateComponents")
      }
    }
    ```

6. Sync the project with Gradle by clicking the **Sync Project with Gradle Files** button (the elephant icon).

    ![GIF of the Gradle sync icon being clicked](/images/fa_aether_tutorial_start_syncgradle.gif)

## Create an immersive activity

To launch your app in VR, your app must include a new Android activity that subclasses the core Android activity `AppSystemActivity`. The sample app has already done this for you in the file `ImmersiveActivity.kt`.

1. Open `app/src/quest/java/com/meta/media/template/ImmersiveActivity.kt`.

    The file's contents are commented out by default.

2. Select the contents of the entire file and uncomment them by clicking **Code** > **Comment with Block Comment** in the toolbar.

    The line `baseTextureAndroidResourceId = R.drawable.skydome` produces an error, but you'll fix that in the next section.

## Import environment assets

`ImmersiveActivity.kt` references the files `environment.glb` and `R.drawable.skydome`. Those files provide the default 3D skybox and landscape, so you'll need to add them to your project.

1. Download those files using this link.

    <section>
    <file-link handle="GEPsfQQ3PhTgsW8BAGWQjAx4m1MLbosWAAAe">
        ZIP of environment.glb and skydome.jpg
    </file-link>
    </section>

2. Unzip the downloaded folder.

3. Follow the step for your operating system.
    * For Windows, in the extracted folder, open the `Assets` subfolder.
    * For Mac, in the extracted folder, open the `__MACOSX/Assets` subfolder.

4. From the `environment` subfolder, drag `environment.glb` (for Windows) or `._environment.glb` (for Mac) to the `app/src/quest/assets` directory in Android Studio.

   **Note**: Mesh assets should always be stored in the `assets/` folder.

5. Return to the extracted folder's `Assets` subfolder.

6. From the extracted folder, drag `skydome.jpg` to the `app/src/quest/res/drawable` directory in Android Studio.

## Update manifests

1. Replace the contents of `quest/AndroidManifest.xml` with this code, which points to your new `ImmersiveActivity.kt` and adds the necessary permissions/features for VR support.

    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <manifest
        xmlns:android="http://schemas.android.com/apk/res/android"
        xmlns:horizonos="http://schemas.horizonos/sdk">

        <horizonos:uses-horizonos-sdk
            horizonos:minSdkVersion="69"
            horizonos:targetSdkVersion="69"
            />

        <uses-feature
            android:name="android.hardware.vr.headtracking"
            android:required="true"
            />

        <uses-feature
            android:name="oculus.software.handtracking"
            android:required="false"
            />
        <uses-permission android:name="com.oculus.permission.HAND_TRACKING" />

        <uses-feature
            android:name="com.oculus.experimental.enabled"
            android:required="true"
            />

        <uses-feature
            android:name="com.oculus.feature.PASSTHROUGH"
            android:required="false"
            />

        <uses-feature
            android:name="com.oculus.feature.VIRTUAL_KEYBOARD"
            android:required="false"
            />
        <uses-feature android:glEsVersion="0x00030001" />

        <uses-feature
            android:name="oculus.software.overlay_keyboard"
            android:required="false"
            />

        <uses-feature
            android:name="com.oculus.feature.RENDER_MODEL"
            android:required="false"
            />
        <uses-permission android:name="com.oculus.permission.RENDER_MODEL" />

        <uses-permission android:name="android.permission.INTERNET" />

        <application
            android:allowBackup="true"
            android:dataExtractionRules="@xml/data_extraction_rules"
            android:fullBackupContent="@xml/backup_rules"
            android:icon="@drawable/icon_media_app"
            android:label="@string/app_name"
            android:roundIcon="@drawable/icon_media_app"
            android:supportsRtl="true"
            android:theme="@style/Theme.AppCompat.NoActionBar">

            <meta-data
                android:name="com.oculus.supportedDevices"
                android:value="quest2|questpro|quest3"
                />
            <meta-data
                android:name="com.oculus.handtracking.version"
                android:value="V2.0"
                />
            <meta-data android:name="com.oculus.vr.focusaware" android:value="true" />

            <uses-native-library
                android:name="libossdk.oculus.so"
                android:required="true"
                />

            <activity
                android:name=".MainActivity"
                android:exported="true"
                android:configChanges="screenSize|smallestScreenSize|screenLayout|orientation"
                android:allowEmbedded="true">
            </activity>
            <activity
                android:name=".ImmersiveActivity"
                android:theme="@android:style/Theme.Black.NoTitleBar.Fullscreen"
                android:launchMode="singleTask"
                android:excludeFromRecents="false"
                android:screenOrientation="landscape"
                android:configChanges="screenSize|screenLayout|orientation|keyboardHidden|keyboard|navigation|uiMode"
                android:exported="true">
                <intent-filter>
                    <action android:name="android.intent.action.MAIN" />
                    <category android:name="com.oculus.intent.category.VR" />
                    <category android:name="android.intent.category.LAUNCHER" />
                </intent-filter>
            </activity>
        </application>
    </manifest>
    ```

2. In `main/AndroidManifest.xml`, delete the `<activity>` block of code that's inside the `<application>` block.

    You delete that code because when you use build variants, Android merges your `main/AndroidManifest.xml` and `quest/AndroidManifest.xml` together, leading to conflicts between the `LAUNCHER` activities if `MainActivity` references aren't removed.

    ```xml
    <activity
        android:name=".MainActivity"
        android:exported="true"
        android:configChanges="screenSize|smallestScreenSize|screenLayout|orientation"
        android:allowEmbedded="true">
        <intent-filter>
            <action android:name="android.intent.action.MAIN" />
            <category android:name="android.intent.category.LAUNCHER" />
        </intent-filter>
    </activity>
    ```

    Once you delete the `<activity>` section, the contents of `main/AndroidManifext.xml` should look like this.

    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <manifest xmlns:android="http://schemas.android.com/apk/res/android">

        <uses-permission android:name="android.permission.INTERNET" />

        <application
            android:allowBackup="true"
            android:dataExtractionRules="@xml/data_extraction_rules"
            android:fullBackupContent="@xml/backup_rules"
            android:icon="@drawable/icon_media_app"
            android:label="@string/app_name"
            android:roundIcon="@drawable/icon_media_app"
            android:supportsRtl="true"
            android:theme="@style/Theme.AppCompat.NoActionBar">
        </application>
    </manifest>
    ```

    Here's what the new manifest does:
    - Adds the required features/permission for VR support on the Quest.
    - Removes the `<intent-filter>` from the `MainActivity` so that it is no longer the `LAUNCHER` activity.
    - Adds the `ImmersiveActivity` and set it as the `LAUNCHER`.

## Deploy and run the app

By this point, you've updated your `LAUNCHER` activity to be the new `ImmersiveActivity`, so your app is ready for you to experience in VR.

1. Plug your Meta Quest headset into your computer.

2. In the top toolbar of Android Studio, in the device dropdown to the left of the green play button (the **Run 'app'** button), set the Android emulator to your headset. For example, **Oculus Quest 3**.

3. Deploy your app to the headset by clicking the **Run 'app'** button in Android Studio.

    ![Run and deploy the app to your Quest](/images/fa_aether_tutorial_immersive_run.gif)

You should see the 2D app appear as a panel in a 3D environment, like this.

<section>
  <embed-video width="100%">
    <video-source handle="GNFrNxwDiL4fP7AGAAmiQDVv1PkybosWAAAF" />
  </embed-video>
</section>

{%include spatial-sdk-shared/spatial-sdk-shared-building-app-content.md %}

## Next steps

- (Optional) Keep exploring the core workflow of Spatial SDK and Spatial Editor in [Continue building your first app](/documentation/spatial-sdk/spatial-sdk-tutorial-shared-content/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/create-new-spatial-sdk-app.md
---
title: Create a new Spatial SDK app
description: This tutorial will give you hands-on practice creating a new Spatial SDK application using Meta Spatial Editor and Meta Spatial SDK.
last_updated: 2025-02-18
---

By the end of this tutorial, you'll have created a new Spatial SDK app and previewed it on your headset. Creating a new Spatial SDK app is the quickest way to get started with the SDK since you aren't constrained by the structure of an existing codebase.

If you'd rather add Spatial SDK to an existing 2D Android app, see [Add Spatial SDK to an existing 2D app](/documentation/spatial-sdk/add-spatial-sdk-to-app/).

## Preview the app on Meta Quest

To download and preview the **CustomComponentsStarter** starter project in your Meta Quest headset, follow these steps.

1. Download the [Meta Spatial SDK Samples](https://github.com/meta-quest/Meta-Spatial-SDK-Samples) zipped folder from GitHub.

    The **CustomComponentsStarter** sample is a basic project containing a Spatial Editor composition and the custom component scripts that you’ll use later on.

2. Once the folder is downloaded, right click on the folder and extract all files.

3. In Android Studio, in the **CodelabStarters** folder, open the **CustomComponentsStarter** project.

    Gradle will begin building, indicated by the progress bar in the lower-right corner of Android Studio.

4. If a **Trust and Open Project** window appears, select **Trust Project**.

5. In your headset, ensure you are on your home screen.

6. Once Gradle has finished building, in the Android Studio toolbar, click the green **Run 'app'** button.

    ![Run and deploy the app to your Quest](/images/fa_aether_tutorial_immersive_run.gif)

    Once the starter app has finished building, it will launch automatically on your headset. It should look like this.

    ![Custom components starter app](/images/spatial-editor-custom-components-start.png)

{%include spatial-sdk-shared/spatial-sdk-shared-building-app-content.md %}

## Next steps

- (Optional) Keep exploring the core workflow of Spatial SDK and Spatial Editor in [Continue building your first app](/documentation/spatial-sdk/spatial-sdk-tutorial-shared-content/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/focus.md
---
title: Focus showcase
description: Build a Quest productivity application with the new Meta Spatial SDK.
last_updated: 2024-09-12
---

## Overview

Focus is a virtual and mixed reality Quest application that shows developers how to build a Productivity app using the Spatial SDK. One of Quest’s primary mixed reality use cases is extending spatial screens. It also offers opportunities to enhance functionality through virtual objects and AI, making it useful for work. To build these applications, you must create spatial objects effectively, store various layouts persistently, spawn objects in coherent locations, and enable intuitive user interaction with panels. The Focus app demonstrates panel and object management, enabling the creation, reuse, and destruction of interactive elements within varied environments. It serves as a practical template for developers interested in creating similar applications, or integrating these features into their own XR projects.

You can [download the Focus app on the Meta Store](https://www.meta.com/experiences/focus/8625912667430203/) and [download its project files from GitHub](https://github.com/meta-quest/Meta-Spatial-SDK-Samples/tree/main/Showcases/focus).

There are several different developer guidelines for reproducing compelling productivity applications below:

1. [Creating spatial objects](#creating-spatial-objects)
2. [Store multiple room configurations](#store-multiple-room-configurations)
3. [Spawn objects relative to user’s position](#spawn-objects-relative-to-users-position)
4. [Create panels and interaction with spatial objects](#create-panels-and-interaction-with-spatial-objects)
5. [Create immersive environments](#create-immersive-environments)

![This gif demonstrates a spatialized experience created with the Spatial SDK](/images/spatial-sdk-focus-1.gif)

## Creating spatial objects

In your application, you will often need to create complex objects by combining multiple entities through object parenting.

Spatial SDK uses an Entity-Component-System (ECS) architecture, enabling developers to create spatial objects with entities. These entities, essentially blank slates, can be outfitted with components like a Transform or Mesh to give it desired properties or behaviors. For detailed information, see Spatial SDK's [ECS documentation](/documentation/spatial-sdk/spatial-sdk-ecs).

While each entity can hold various components, only one of each type is allowed. Objects such as clocks, speakers, and timers in Focus are built from multiple entities. The speaker shown below is simpler and consists of only two entities. The first entity incorporates the speaker.glb 3D model, while the second displays an image indicating the ON and OFF states.

![A simple speaker component that consists of two entities](/images/spatial-sdk-focus-2.gif)

The clock and timers are also composed by two entities, the first with a Mesh component (*clock.glb* and *timer.glb*), and the second with a Panel component linked to a specific layout for each element.


Create an entity with a Mesh component:

```
// Timer.kt
val timerObj = Entity.create(
    Mesh(mesh = Uri.parse("timer.glb")),
    Scale(0.1f),
    Grabbable(true, GrabbableType.PIVOT_Y)
    Transform(Pose(Vector3(0f)))
)
```

Create an entity with a Panel component:

```
// Timer.kt

var id = getDisposableID()
val _width = 0.18f
val _height = 0.18f
val _dp = 1150f

ImmersiveActivity.instance.get()?.registerPanel(
    PanelRegistration(id) {
        layoutResourceId = R.layout.timer_layout
        config {
            themeResourceId = R.style.Theme_Focus_Transparent
            width = _width
            height = _height
            layoutWidthInDp = _dp
            layoutHeightInDp = _dp * (height / width)
            includeGlass = false
        }
        panel {
            rootView?.findViewById<TextView>(R.id.totalTime)?.text = totalTime.toString() + "'"
        }
    }
)

val timerPanel: Entity = Entity.create(
    Panel(id).apply { hittable = MeshCollision.NoCollision },
    Transform(Pose(Vector3(0f, 0f, 0.025f), Quaternion(0f,180f,0f)))
)

// To link this objects, we need to set one as the parent of the other:
timerPanel.setComponent(TransformParent(timerObj))
```

![A simple timer object](/images/spatial-sdk-focus-3.png)

For composed objects, it's best to attach the Grabbable component solely to the parent. This ensures that objects remain unified during movement. Additionally, consider deactivating the hittable property on child objects. This prevents them from obstructing the raycast when interacting with the parent object, especially if it's positioned behind a child object.

### Composed objects

```
// Disabling hittable for Mesh component
Mesh(Uri.parse("mesh://box")).apply { hittable = MeshCollision.NoCollision }

// Disabling hittable for Panel component
Panel(id).apply { hittable = MeshCollision.NoCollision }
```

**Note**: The Transform of an object that has a TransformParent is relative to the parent. If you need the global (in other words, non-relative) transform of an entity, you can use Spatial SDK's getAbsoluteTransform() function.

Spatial Audio, a standout feature in Spatial SDK, reproduces audio from a specific point in space, giving the impression that the sound is coming from a particular direction. You can also link audio to an entity, ensuring that the sound moves along with it.

To play spatial sound as a child of an entity, follow the method below:

```
val timerSound = SceneAudioAsset.loadLocalFile("audio/timer.wav")
scene.playSound(timerSound, entity, 1f)
```

### Custom helper functions

Custom helper functions in the [Utils.kt](https://github.com/meta-quest/Meta-Spatial-SDK-Samples/blob/main/Showcases/focus/app/src/main/java/com/meta/theelectricfactory/focus/Utils.kt) file streamline repetitive and common actions for spatial apps.
For example, the `getChildren()` function returns a list of entities that are children of an entity:

```
fun getChildren(parent: Entity): MutableList<Entity> {
    var children: MutableList<Entity> = mutableListOf()
        val allChildren = Query.where { has(TransformParent.id) }
        for (child in allChildren.eval()) {
            val _parent = child.getComponent<TransformParent>().entity
            if (parent == _parent) {
                children.add(child)
            }
        }
        return children
    }
```

## Store multiple room configurations

Why is this important? To maintain application state between sessions, use Android Shared Preferences (or an equivalent) to save data that persists after the application has been closed.

Focus enables the creation of multiple objects, and each project requires  storing various data types locally on your device. These include the position and rotation of spatial objects, states, associated text, and other properties. While Android Shared Preferences can be used for this purpose, SQLite may be a better solution for more complex data structures.

To add a SQLite database to your project you can follow this [Android Developer SQLite Guide](https://developer.android.com/training/data-storage/sqlite).

Focus has implemented a [DatabaseManager](https://github.com/meta-quest/Meta-Spatial-SDK-Samples/blob/main/Showcases/focus/app/src/main/java/com/meta/theelectricfactory/focus/DatabaseManager.kt) class to create, save, and retrieve data from a database.

There are five tables with different elements and attributes: Projects, Unique Assets, Tools, Sticky Notes and Tasks. Implemented methods include the DatabaseManager to create, get, update, and delete the elements in these tables.

### Use components to save and retrieve object data and state

In Focus, the elements are split into two categories:

- Unique Assets: Elements that are unique in the scene and cannot be deleted, like the Clock, Speaker, Tasks Panel, and AI Exchange Panel.
- Tools: Elements the user can create and delete, like Boards, Sticky Notes, Tasks, Labels, Arrows, Shapes, Stickers, and Timers.

The database must be updated whenever these elements change state or position.

ECS is the core of Spatial SDK. To identify different objects in Focus, there are three custom components to attach to the entities:

- UniqueAssetComponent: `./app/src/main/java/com/meta/theelectricfactory/focus/UniqueAssetComponent.kt`
- ToolComponent: `./app/src/main/java/com/meta/theelectricfactory/focus/ToolComponent.kt`
- TimeComponent: `./app/src/main/java/com/meta/theelectricfactory/focus/TimeComponent.kt`

To create a Component, your class must inherit from `ComponentBase()`.

### Unique Asset component

```
class UniqueAssetComponent (
    uuid: Int? = 0,
    type: AssetType = AssetType.CLOCK ) : ComponentBase() {

    var uuid by IntAttribute("uuid", R.id.UniqueAssetComponent_uuid, this, uuid)
    var type by EnumAttribute("type", R.id.UniqueAssetComponent_type, this, AssetType::class.java,  type)

    override fun typeID(): Int {
        return UniqueAssetComponent.id
    }
    companion object : ComponentCompanion {
        override val id = R.id.UniqueAssetComponent_class
        override val createDefaultInstance = { UniqueAssetComponent() }
    }
}
```

You must register your component in your activity to use it:

```
//ImmersiveActivity.kt
componentManager.registerComponent<UniqueAssetComponent>(UniqueAssetComponent.Companion)
```

### Create a helper system to update objects’ positions

Focus uses a helper system that updates the position and rotation of objects in a database. It uses Spatial SDK systems and queries to check if an object has been grabbed and updates its position and rotation accordingly.

1. Create a class that inherits from SystemBase.
2. Register the system in your activity.
3. In the execute function, create a query to pull data from the data model, and get all elements that have a UniqueAsset or Tool component.
4. Check if any element in the lists has been grabbed. If so, update the position and rotation of the element in the database.
5. Consider running this process every x amount of time to improve performance.

```
// ImmersiveActivity.kt
systemManager.registerSystem(DatabaseUpdateSystem())

// DatabaseUpdateSystem.kt
class DatabaseUpdateSystem : SystemBase() {
    private var lastTime = System.currentTimeMillis()

    override fun execute() {

        if (ImmersiveActivity.instance.get()?.appStarted == false) return

        val currentTime = System.currentTimeMillis()

        // if there is no current project, we don't update database
        if (ImmersiveActivity.instance.get()?.currentProject == null) {
            lastTime = currentTime
        }

        // Check if objects are being moved and save new position
        // We do this each 0.2 seconds to improve performance
        val deltaTime = (currentTime - lastTime) / 1000f
        if (deltaTime > 0.2) {
            lastTime = currentTime

            // Update pose of tool assets
            val tools = Query.where { has(ToolComponent.id) }
            for (entity in tools.eval()) {
                val asset = entity.getComponent<ToolComponent>()
                val pose = entity.getComponent<Transform>().transform
                val isGrabbed = entity.getComponent<Grabbable>().isGrabbed

                if (isGrabbed) {
                    if (asset.type != AssetType.TIMER) ImmersiveActivity.instance.get()?.DB?.updateAssetPose(asset.uuid, asset.type, pose)
                }
            }

            // Update pose of unique assets
            val uniqueAssets = Query.where { has(UniqueAssetComponent.id) }
            for (entity in uniqueAssets.eval()) {
                val uniqueAsset = entity.getComponent<UniqueAssetComponent>()
                val pose = entity.getComponent<Transform>().transform
                val isGrabbed = entity.getComponent<Grabbable>().isGrabbed

                if (isGrabbed) ImmersiveActivity.instance.get()?.DB?.updateUniqueAsset(uniqueAsset.uuid, pose)
            }
        }
    }
}
```

You can find the complete code in [DatabaseUpdateSystem.kt](https://github.com/meta-quest/Meta-Spatial-SDK-Samples/blob/main/Showcases/focus/app/src/main/java/com/meta/theelectricfactory/focus/DatabaseUpdateSystem.kt).

### Detect keyboard events

You can detect keyboard events in Focus, like when a user has finished writing text. This is useful for updating text in the database. To do this, follow these steps:

1. Add two properties to the EditText in the .XML file: android:inputType="text" and android:imeOptions="actionDone".
2. Set an action listener to the EditText using setOnEditorActionListener to perform an action once the user finishes writing.
3. For longer texts that span multiple lines, add a TextWatcher to the EditText to detect when the user stops writing.
4. Use the addEditTextListeners function from [Utils.kt](https://github.com/meta-quest/Meta-Spatial-SDK-Samples/blob/main/Showcases/focus/app/src/main/java/com/meta/theelectricfactory/focus/Utils.kt) to add these listeners to any EditText and choose whether to update the text when the action is done, or when the user stops writing.

```
// .xml file
<EditText
…
    android:inputType="text"
    android:imeOptions="actionDone" />

// Utils.kt
fun addEditTextListeners(editText: EditText?, onComplete: () -> (Unit), updateWithoutEnter:Boolean = false ) {

    // Detect Enter keyboard (Done) to perform action
    if (!updateWithoutEnter) {
        var enterTime:Long = 0
        val waitingInterval:Long = (0.5f * 1000).toLong() // 0.5 seconds

        editText?.setOnEditorActionListener { v, actionId, event ->
            if (actionId == EditorInfo.IME_ACTION_DONE || event?.action == KeyEvent.ACTION_DOWN && event.keyCode == KeyEvent.KEYCODE_ENTER) {

                // To avoid multiple events to trigger the same action
                if (System.currentTimeMillis() - enterTime >= waitingInterval) {
                    enterTime = System.currentTimeMillis()
                    onComplete()
                    return@setOnEditorActionListener true
                }
            }
            false
        }
    // In cases that virtual keyboard doesn't have an Enter (Done) button, like in multiline texts, we wait 1 second after user finished writing to perform the action
    } else {
        var lastTextChangeTime:Long = 0
        val typingInterval:Long = 1 * 1000
        val handler = Handler(Looper.getMainLooper())

        editText?.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) { }

            // update lastTime if user is still writing
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                lastTextChangeTime = System.currentTimeMillis()
            }

            override fun afterTextChanged(s: Editable?) {
                handler.postDelayed({
                    // Wait to perform action
                    if (System.currentTimeMillis() - lastTextChangeTime >= typingInterval) {
                        onComplete()
                    }
                }, typingInterval)
            }
        })
    }
}
```

## Spawn objects relative to user’s position

Ensuring that new objects spawn within the user’s field of view is crucial. The visibility confirms to the user that the object has been created.

To ensure new elements appear in front of a user, their location and viewing direction must be considered.

Steps to use:

1. Get the user's position using the getHeadPose() function.
2. Determine the distance from the user where you want the object to be shown.
3. Calculate the new position using Vector3.Forward and modify the height to match the user's head height.
4. Ensure the spatial object faces the user by calculating the lookRotation and rotating it 180 degrees on the Y axis.
5. Use the placeInFront() function to place the object in front of the user, incorporating an offset vector for positioning elements in specific poses relative to the user.

```
// Utils.kt

fun getHeadPose(): Pose {
    val head =
        Query.where { has(AvatarAttachment.id) }
            .eval()
            .filter { it.isLocal() && it.getComponent<AvatarAttachment>().type == "head"}
            .first()
    return head.getComponent<Transform>().transform
}

fun placeInFront(entity: Entity?, offset: Vector3 = Vector3(0f), bigPanel:Boolean = false, nonPanel:Boolean = false) {
    val headPose:Pose = getHeadPose();

    val isToolbar = entity!! == ImmersiveActivity.instance.get()?.toolbarPanel

    // We treat toolbar and big panels differently from other objects.
    val height: Float = if (isToolbar) 0.35f else 0.1f
    var distanceFromUser: Float = if (bigPanel) 0.9f else 0.7f

    // Having the users position, we place the entity in front of it, at a particular distance and height
    var newPos = headPose.t + headPose.q * Vector3.Forward * distanceFromUser
    newPos.y = headPose.t.y -height

    // If there is an offset vector, we place the object at the vector position (using user's position as reference)
    if (offset != Vector3(0f)) {
        newPos = headPose.t +
                headPose.q * Vector3.Right * offset.x +
                headPose.q * Vector3.Forward * offset.z

        newPos.y = headPose.t.y + offset.y
    }

    // Add rotation to look in same vector direction as user
    var newRot = Quaternion.lookRotation(newPos - headPose.t)
    // Rotate 180 degrees to face user in case of non panel objects
    if (nonPanel) newRot *= Quaternion(0f, 180f, 0f)

    entity.setComponent(Transform(Pose(newPos, newRot)))
}
```

## Create panels and interaction with spatial objects

Focus Projects features 12 main spatial panels, including the Home Panel, the Toolbar, and its sub-panels. Users can create additional panels by generating Sticky Notes, Timers, WebViews, or Spatial Tasks.

You can create panels, make them grabbable, and give them functionality.

![You can create panels, make them grabbable, and give them functionality.](/images/spatial-sdk-focus-4.jpg)

### Create transparency and spatial text panels

To effectively use spatial text, design a new theme style and set the windowBackground property to transparent, creating a panel with a transparent background.

```
//themes.xml
<style name="Theme.Focus.Transparent" parent="Base.Theme.Focus">
…
  <item name="android:windowBackground">@android:color/transparent</item>
…
 </style>
 ```

Next, apply the theme to the panel configuration. Set the includeGlass attribute to false in the PanelConfigOptions if you want to hide the panel.

```
val panelRegistration = PanelRegistration( R.layout.activity_main) {
    config {
        themeResourceId = R.style.Theme_Focus_Transparent
        width = 0.5f
        height = 0.5f
        includeGlass = false
    }
    activityClass = MainActivity::class.java
}
```

![Demonstrating transparency and spatial text panels](/images/spatial-sdk-focus-5.jpg)

To attach a spatial text to an object, check our explanation of Composed Objects in the section Creating spatial objects: object hierarchy.

## Create immersive environments

Immersive VR environments transport users to new or distant places. The quality of the environment can make or break the immersion. When done well, they can help a user focus on application content more effectively.

Focus offers three immersive environments for project development, each consisting of a 3D model, a skybox, and scene lighting. These elements function independently, but are combined in Focus to form a cohesive concept.

![image](/images/spatial-sdk-focus-6.gif)

### Load and switch between panoramas (skybox)

To create a panorama or skybox, you can use Spatial SDK's skybox Mesh primitive, and set a 360 image to the baseTextureAndroidResourceId attribute:

```
skybox =  Entity.create(
Mesh(Uri.parse("mesh://skybox")),
Material().apply {
baseTextureAndroidResourceId = R.drawable.skybox1
             unlit = true // Prevent scene lighting from affecting the skybox
       },
Transform(Pose(Vector3(0f)))
)
```

Use a single entity for multiple skyboxes in your scene due to the large size of skybox textures. Change the texture of this entity whenever you need to display a different skybox.

```
skybox.setComponent(
    Material().apply {
        baseTextureAndroidResourceId = R.drawable.skybox2
        unlit = true
    },
)
```

To improve performance, create a system that progressively loads skyboxes when you need to display them simultaneously or combine them.

### Load and switch between 3D model scenes

You can create 3D environments that resemble any custom 3D object in your scene. You can do this by creating an entity with a mesh component in the scene.xml file or directly from your activity. For Focus, the direct configuration method is used.

```
environment = Entity.create(
    Mesh(mesh = Uri.parse("environment1.glb")),
    Visible(false),
)
```

Like any other 3D object, environments, tend to be larger than other models. If you plan to use multiple environments, similar to the skyboxes recommendation, consider changing the mesh model instead of creating a separate entity.

`environment.setComponent(Mesh(mesh = Uri.parse("environment2.glb")))`

### Change the lighting environment

You can set your scene’s lighting in two ways.

The first option is using a .env file. You probably want to use your skybox texture to generate this file. This ensures the lighting will match the colors and properties of your skybox.

`scene.updateIBLEnvironment("skybox.env")`

Set an ambience and directional light with vectors:

```
scene.setLightingEnvironment(
    Vector3(2.5f, 2.5f, 2.5f), // ambient light color (none in this case)
    Vector3(1.8f, 1.8f, 1.8f), // directional light color
    -Vector3(1.0f, 3.0f, 2.0f), // directional light direction
)
```

Focus has three different environments. There are different light configurations for each one, including the introduction lighting:

```
private fun setLighting(env: Int) {
    when (env) {
        -1 -> {
            scene.setLightingEnvironment(
                Vector3(2.5f, 2.5f, 2.5f), // ambient light color (none in this case)
                Vector3(1.8f, 1.8f, 1.8f), // directional light color
                -Vector3(1.0f, 3.0f, 2.0f), // directional light direction
            )
        }
        0 -> {
            scene.setLightingEnvironment(
                Vector3(1.8f, 1.5f, 1.5f),
                Vector3(1.5f, 1.5f, 1.5f),
                -Vector3(1.0f, 3.0f, 2.0f),
            )
        }
        1 -> {
            scene.setLightingEnvironment(
                Vector3(1.5f, 1.5f, 1.5f),
                Vector3(1.5f, 1.5f, 1.5f),
                -Vector3(1.0f, 3.0f, 2.0f),
            )
        }
        2 -> {
            scene.setLightingEnvironment(
                Vector3(3.5f, 3.5f, 3.5f),
                Vector3(2f, 2f, 2f),
                -Vector3(1.0f, 3.0f, 2.0f),
            )
        }
    }
}
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/geo-voyage-component-system.md
---
title: Custom entity component system (panels and virtual objects)
description: Learn how the Geo Voyage showcase uses a custom component system to create panels and other virtual objects.
last_updated: 2024-09-20
---

## UI

This application uses one main panel object for all UI. The layout and UI elements were created with [Jetpack Compose](https://developer.android.com/compose), and are rendered into the scene via a Spatial SDK PanelSceneObject. The design follows [Material Design](https://m3.material.io/) standards, and was engineered to be similar to a landscape tablet screen view.

This panel floats to the right of the globe, and is the main navigation means for the user. Tapping on the list items on the right side of this panel initiates the 4 corresponding play modes – each with their own content, which appears in the middle of the panel on elevated green surfaces. Additionally, the cog button on the upper right exposes a Settings menu with various controls over application behavior, while the title text at the top displays persistent relevant information about or of the current play mode.

![Main UI panel](/images/geo-ui.png)

## Custom components and systems

Six custom components and systems were created for this application.

* **Spinnable**: Allows you to spin the globe.
* **GrabbableNoRotation**: Enables you to move the globe and panel around your play space without rotation.
* **Tether**: Keeps the panel on a short leash near the globe, ensuring it always rotates to face you.
* **Pinnable**: Allows you to drop a pin on the globe during explore mode.
* **LandmarkSpawn**: Manages the spawning and management of landmark models.
* **Spin**: Gradually spins the cloud model around the globe.

### Spinnable

The **Spinnable** component and **SpinnableSystem** ECS system manage all globe rotation behaviors. When you point your controller or hand at the globe and grab it, you can spin it around. This rotation behavior includes clamping the pitch rotation at 45 degrees if you pitch your controller while holding the globe, or applying yaw rotation if you rotate your controller on the y-axis while holding the globe.

![Spinnable](/images/geo-spinnable.gif)

Two behaviors enhance the spinning rotation behavior, making it more engaging and intuitive:

* If you point your controller at the globe and press the A or X button to grab it, the globe will continue to spin as long as the button is held down and the controller is rotating—even if you are no longer pointing at the globe. This allows you greater flexibility to rotate the globe any way you want without having to repeatedly grab and rotate to view a point on the opposite side of the globe from your current position.
* If you fling your wrist and release the spin hold button simultaneously, the globe will spin about its y-axis, smoothly slowing down until it stops. Note that this inertia behavior applies to the yaw rotation, but not to the pitch rotation.

The `SpinnableSystem` follows an architectural pattern evident in several custom ECS implementations described on this page. A query retrieves the corresponding `SceneObjects` for the entities with the Spinnable component, and input listeners attach to those scene objects. When you press the designated button while pointing at the object, the triggered input handler stores an instance of a data class encapsulating all the data needed for system processing. Later, in the execute function, all grabbed entities and their rotation behavior are processed. The data class for the `SpinnableSystem` grabbed entities is structured as follows:

```
private data class SpinningInfo(
    // the Entity which represents either the user's hand or held controller –
    // whichever "grabbed" the Spinnable
    val inputSource: Entity,


    // the "grabbed" Spinnable Entity
    val entity: Entity,


    // yaw and pitch offsets in radians of the vectors which represents the
    // direction from the "grabbed" Entity to the controller, and the
    // controller's forward vector
    val initialYawOffset: Float,
    val initialPitchOffset: Float,


    // the initial absolute rotation of the "grabbed" Entity. Used in
    // conjunction with the initial offsets to determine the new rotation
    val initialRotation: Quaternion,


    // cached value indicating whether or not the Entity has a
    // GrabbableNoRotation component also attached to it, so we know to disable
    // it until after the spin grab button is released
    val hasGrabbable: Boolean = false,


    // both used for calculating the rotation speed, and spin inertia for
    // gradually slowing down
    var lastYawOffsetDeg: Float = 0f,
    var yawInertiaDeg: Float = 0f
)
```

The Spinnable component includes properties that influence rotation behavior:

* **Size**: A float value used in the yaw rotation calculation. It determines the rotation amount of the grabbed spinnable object per degree of rotation of the user's controller. This calculation considers the arc length of the controller's rotation relative to the distance between the spinnable object and the controller, ensuring a natural rotation amount regardless of the user's distance from the object.
* **Drag**: A float value that determines the rate at which spinning decelerates to zero when the user flicks their wrist and releases the hold button simultaneously. A higher value results in quicker cessation of rotation.
* **Spinnable.Companion.MAX_PITCH_RAD**: A float representing a static constant within the Spinnable component that sets the maximum pitch rotation a user can apply to an entity.

The final rotation behavior and implementation involve complex 3D mathematical calculations not covered here. For further explanation on this implementation, refer to the commented function `SpinnableSystem.processSpinnables` after familiarizing yourself with the basics of the Spatial SDK, and the fundamentals of Vector3 and Quaternion operations.


### GrabbableNoRotation

This system behaves nearly identically to the built-in Spatial SDK `Grabbable` Component, except that it doesn't alter the grabbed entity's rotation. This was built to allow the user to move the globe around their play space without affecting the globe's spinning.


### Tether

The Tether component and TetherSystem ECS system ensure that panels float next to the globe in 3D space, even when you grab and move the globe within your play space. Typically, the built-in TransformParent component could achieve this. However, in this scenario, using the SpinnableSystem to rotate the globe would also spin the panel entities with the Tether component around the globe, which is undesirable.

![Tether](/images/geo-tether.gif)

In addition to anchoring the panel positions around the globe, the TetherSystem always orients the panels to face you, even when you grab and move the globe. This is achieved through several steps:

1. Calculate the vector representing the direction from the Tether anchor entity (the entity to which the Tether entity is tethered) to your head.
2. Determine the target position of the panel using that vector, a distance offset along that vector, and a rotation around the yaw of the tether anchor entity.
3. Compute the target rotation, a quaternion representing a rotation around the world up vector, with the forward vector being the cross product of the world up vector and the vector representing the direction from the Tether anchor entity to the new target position.
4. Smoothly interpolate the panel Transform position and rotation to the calculated target position and target rotation.

This tethering behavior involves numerous 3D mathematical calculations not covered here. For more explanation on this implementation, see the commented function `TetherSystem.processTethers` after familiarizing yourself with the Spatial SDK's basics, and the basics of Vector3 and Quaternion operations.


### Pinnable

When you select a point on the globe during the Explore play mode, the system drops an entity with a pin mesh at that location. MainActivity is immediately notified of the geo coordinates where the pin was placed. Subsequently, application services are activated to fetch and display information about the corresponding location on Earth. You can find more details about these services on the [Google Maps API](https://developers.google.com/maps/) page and [Llama3](https://github.com/meta-llama/llama3) page.

![Pinnable](/images/geo-pinnable.gif)

The custom ECS implementation for pinnable entities consists of a Pinnable component and a PinnableSystem. This setup manages the pin entity's behavior and notifies MainActivity about the location of the pin drop. This process follows a similar implementation pattern as other custom ECS, where a Query identifies the entities and their scene objects, and attaches an input listener to manage the select event.

### LandmarkSpawn

This system is structured differently than other custom ECS described on this page and uses the Spatial SDK in an atypical way. It is designed to demonstrate how you can implement a system that consumes a data object and parses it to add entities and components to your scene after the initial app launch. A potential use case involves fetching data from a remote server that describes entities to be spawned in your scene. Typically, you would use the `AppSystemActivity.inflateIntoDataModel` function to populate a scene with your entities and might fetch a `scene.xml` from a remote source to do so. However, this implementation shows how you might have already inflated your `scene.xml` into the data model but want to dynamically add entities afterward.

In our example, the local file at `app/src/main/res/xml/landmarks.xml` is loaded and parsed when the system initializes. Each node in this file represents a landmark object that is spawned on the globe, and the node's child elements describe how to position and orient it properly. The `Entity.create` function is then used to spawn the entity and attach the appropriately configured component objects. Here is a sample of a landmark node:

```
<landmark
    name="Great Egyptian Pyramids"
    description="Three majestic pyramids in Giza, built around 2580 BC, served as ancient tombs for Pharaohs Khufu, Khafre, and Menkaure. They are engineering marvels of limestone and granite, showcasing the architectural genius of ancient Egypt."
    latitude="29.979167"
    longitude="31.134167"
    model="pyramid.glb"
    scale="1.0"
    yaw="45"
    zOffset="0.37" />
```

Note that a query during the execute function is still used to retrieve all references to the SceneObjects corresponding to the landmark entities. This retrieval must occur after the system initializes and spawns the entities because ECS system registration and initialization happen during the AppSystemActivity.onCreate call, before AppSystemActivity.onSceneReady execution.

In addition to spawning the landmark entities, the LandmarkSpawnSystem serves three other purposes:

* Display the landmark entities if you enter the Explore play mode; otherwise, hide them.
* Slightly scale up the landmark entities when they face you on the globe.
* Notify MainActivity when you click on a landmark, prompting it to display the landmark's information on the panel.

### Spin

In this application, the simplest custom ECS includes the `Spin` component and the `SpinSystem`. These elements work together to rotate an entity's transform around a specified axis at a defined speed. Specifically, this functionality is applied to rotate the cloud model around the globe.

![Spin component rotating clouds](/images/geo-spin.gif)

* **Spin**: This component requires two parameters: `speed: Float` and `axis: Vector3`.

* **SpinSystem**: This system performs several steps to rotate entities:

    1. Using a Query, it collects entities in the scene that have both the Transform and Spin components.
    2. It then iterates through these entities, calculates the new rotation in the form of a Quaternion, and applies this rotation to each entity's Transform component.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/geo-voyage-overview.md
---
title: Geo Voyage overview
description: Overview of the Geo Voyage showcase.
last_updated: 2024-09-20
---

Geo Voyage is a mixed reality app that demonstrates to developers how to create applications that enhance learning experiences for Quest users through the new Spatial SDK. Quest enables users to view virtual objects in their environment, transport themselves to immersive settings, and interact with AI agents powered by Meta’s open-sourced models such as Llama 3. Developers can utilize these elements to craft experiences that enhance learning on Quest.

This app guides you through the process of integrating Llama 3 with additional tools such as Wit.AI and Amazon Bedrock to develop an AI learning agent, integrate panels with virtual objects using a Custom Entity Component System (ECS), and use real-world data from Google Maps API to transition users from a pin on a virtual object to a fully immersive view of the actual world.

You can [download the Geo Voyage app on the Meta Store](https://www.meta.com/experiences/geo-voyage/8230251250434003/), and [download its project files from GitHub](https://github.com/meta-quest/Meta-Spatial-SDK-Samples/tree/main/Showcases/geo_voyage).

Below are developer guidelines related to reproducing compelling educational applications:
* [Process audio with Wit.AI](/documentation/spatial-sdk/geo-voyage-process-audio/)
* [Query with Llama 3 using Ollama and Amazon Bedrock](/documentation/spatial-sdk/geo-voyage-query-llama/)
* [Panels & Virtual Objects (Custom Entity Component System)](/documentation/spatial-sdk/geo-voyage-component-system/)
* [Transport users to VR with Google Maps API](/documentation/spatial-sdk/geo-voyage-transport-users/)

![All features of Geo Voyage](/images/geo-overview.gif)

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/geo-voyage-process-audio.md
---
title: Process audio with Wit.AI
description: Learn how the Geo Voyage showcase uses Wit.AI to detect and transcribe audio.
last_updated: 2024-09-20
---

This application uses Wit.ai for speech-to-text transcription and understanding the user. By transcribing the user's speech and understanding what the user is saying or asking, the application can react appropriately by taking some predetermined action. For demonstration purposes, this application uses only a small number of intents and entities, defined and trained in the Wit.ai web dashboard, to determine whether to query Llama with the transcribed speech.

Wit.ai can enhance your applications significantly, including creating bots for chatting and enabling voice control over smart home devices. To learn more, see Wit’s [Get Started](https://wit.ai/docs/quickstart) page.

![Wit AI transcribing the user's speech](/images/geo-wit.gif)

## Core files

The core files for this integration are located within the directory `app/src/main/java/com.meta.pixelandtexel.geovoyage/services/witai` and its subfolders.

```
/services
    /witai
        IWitAiServiceHandler.kt
        WitAiFlowService.kt
        WitAiService.kt


        /enums
            ...
        /models
            ...
```

## Getting a transcription and understanding

The main entry point for using Wit.ai in this application is the `WitAiService.startSpeechToText` function. This function was adapted from a [Wit.ai example Android project](https://wit.ai/docs/android/latest) and was subsequently ported to Kotlin.

The `startSpeechToText` function performs the following actions:

* Starts the device microphone input.
* Initiates an HTTP streaming request to the Wit.ai `POST /speech` endpoint.
* Writes the microphone input data to the request stream.
* Stops the streaming and finishes the request when the user selects stop or pauses their speech.
* Reads the response stream from Wit.ai, parsing partial transcriptions.
* Returns the final understanding when the response finishes.

**Note**: While it could be argued that the `startListening` implementation could have more strictly followed the separation-of-concerns principle, the decision was made to consolidate the microphone recording and Wit.ai request streaming functionalities into a single service for demonstration purposes and ease of use in this application.

The `startSpeechToText` function accepts one `IWitAiServiceHandler` argument and returns a `WitAiStartResult` enum value. The `WitAiStartResult` enum should be used to handle any errors that may occur when attempting to start the service. The `IWitAiServiceHandler` argument is used to accept callbacks from the service and handle the events and results appropriately.

The final callback function `IWitAiServiceHandler.onFinished` receives an instance of the `WitAiUnderstoodResponse` model. This should be used by the calling function to take any appropriate action based on the transcription and matched Wit.ai intents, entities, and traits.

**Note**: This service uses multithreading because it is a long-running operation that streams the response back as Wit.ai transcribes what the user says.

### Example usage

You can see an example of usage in the `startListening` function located in the file `/app/src/main/java/com/meta/pixelandtexel/geovoyage/viewmodels/AskEarthViewModel.kt`. This function includes updates to UI and error handling.

```
val startResult = WitAiService.startSpeechToText(
    object : IWitAiServiceHandler {
        override fun onStartedListening() {
            // (optional) indicate to the user that the microphone input has
            // started
        }


        override fun onAmplitudeChanged(amplitude: Int) {
            // (optional) indicate to the user a change in the microphone's
            // detected volume
        }


        override fun onFinishedListening() {
            // (optional) indicate to the user that the microphone input has
            // stopped
        }


        override fun onPartial(partial: String) {
            // (optional) update our UI to show a partial transcription
        }


        override fun onFinished(result: WitAiUnderstoodResponse) {
            // use the understood result to take the appropriate action, or
            // simply display or use the result.text transcription value
        }


        override fun onError(reason: String) {
            // handle request error
        }
    }
)


if (startResult != WitAiStartResult.SUCCESS) {
    // handle a microphone start error
}
```

### Finished speaking detection

Any app or service that accepts user voice prompts should automatically detect when the user has finished speaking. This feature eliminates the need for the user to manually indicate that they've stopped speaking. However, it's complicated to implement this type of feature. Computer scientists and audio engineers employ various voice activity detection (VAD) techniques to detect human speech and to identify when it starts or stops. These techniques include:

* Spectral analysis
* Zero-crossing rate (ZCR)
* Machine learning
* Energy and silence detection

Implementing a robust VAD solution was beyond the scope of this project. However, you can find a basic implementation of energy and silence detection in the `startListening` function, which utilizes the `NoiseLevelAdjuster` class and utility functions in `app/src/main/java/com.meta.pixelandtexel.geovoyage/utils/AudioUtils.kt.`.

Here’s a high-level breakdown of this implementation workflow:

1. Maintaining a smoothed running average of the absolute amplitude of the audio signal over a short period.
2. Using that baseline noise level and an arbitrary adjustment multiplier to set a silence threshold.
3. Comparing the volume level with the silence threshold to determine if the user has stopped speaking.
4. Stopping the microphone if the user has not spoken for a given period of time.

While this solution is not perfect, it functions correctly most of the time. Due to its imperfections, a toggle is available in the Settings menu to disable the auto-stop recording functionality, should you find that the feature is not reliable in your noise environment.

## Using the understanding

After your application receives an understanding of the user's speech from Wit.ai in the form of a `WitAiUnderstoodResponse` model, you need to decide the next action. You might choose to display or utilize the transcribed text from the user's speech. Alternatively, you could determine an appropriate action based on the intents, entities, and traits detected in the user's utterance.

For this application, a simple check determines if there were any matched entities and intents in the user's speech to decide if the transcription should be passed to Llama 3 as a query. This method acts as a filtering mechanism, ensuring that only questions related to Earth's geography, history, and culture are answered.

The function `WitAIFlowService.shouldSendResponseToLlama` includes the core implementation of this filtering. In the function body, it first accumulates the sets of entities, intents, and traits found within the `WitAiUnderstoodResponse` object.

```
fun shouldSendResponseToLlama(response: WitAiUnderstoodResponse): Boolean {
    // ...


    // accumulate the Wit.ai objects found within our response
    val responseEntities: Set<WitAiEntity> = getNamedEntitiesFromResponse(response)
    val responseIntents: Set<WitAiIntent> = getNamedIntentsFromResponse(response)


    // ...
}
```

Then the function counts a simple intersection of the detected response objects with predefined sets of entities and traits suitable for a Llama query.

```
// ...


// determine how many of our response Wit.ai objects intersect with our
// predetermined list of objects which are acceptable for a Llama query
val numEntitiesMatch = responseEntities.intersect(allowedEntitiesForLlama).size
val numIntentsMatch = responseIntents.intersect(allowedIntentsForLLama).size


// ...
```

The system returns a check to determine if the response contains an acceptable number of detected entities and traits that meet or exceed a given threshold. Specifically, it checks if at least one intent and one entity are detected.

```
 // ...


    return numEntitiesMatch > 0 && numIntentsMatch > 0
```

Here's the full function.

```
fun shouldSendResponseToLlama(response: WitAiUnderstoodResponse): Boolean {
    // accumulate the Wit.ai objects found within our response
    val responseEntities = getNamedEntitiesFromResponse(response)
    val responseIntents = getNamedIntentsFromResponse(response)


    // determine how many of our response Wit.ai objects intersect with our
    // predetermined list of objects which are acceptable for a Llama query
    val numEntitiesMatch = responseEntities.intersect(allowedEntitiesForLlama).size
    val numIntentsMatch = responseIntents.intersect(allowedIntentsForLLama).size


    return numEntitiesMatch > 0 && numIntentsMatch > 0
}
```


### Improved filtering

While out-of-scope for this project, a more robust solution would involve taking different actions based on which intents or entities are matched. In the scenario of determining whether to query Llama, you could pre-define a set of queries with injectable components. You would then select the query that matches the detected intent and inject any matched entities into the query.

```
country_fact_query = "What is one interesting fact about the country {{country_name}}"


if responseIntent == "country_fact" && responseEntity.type == "country"
    formatted_query = country_fact_query.replace("{{country_name}}", responseEntity.value)
    queryLlama(formatted_query)
```

This solution provides you with greater control over the queries sent to Llama, reducing the risk of mismatched queries due to imperfect speech transcription. The effectiveness of this approach depends on how you define intents and entities in your Wit.ai app and how well the queries are trained.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/geo-voyage-query-llama.md
---
title: Query with Llama 3
description: Learn how the Geo Voyage showcase uses Llama 3 to retrieve and generate information.
last_updated: 2024-09-19
---

This application uses Meta's LLM Llama 3 8B to teach users about our planet's geography, cultures, ecology, and history. Here's how it's used in each of the four play modes.

* **Ask Earth**: Retrieves answers to users' questions.
* **Explore**: Gathers information about a selected location on the globe and generates short descriptions for landmarks.
* **Today in History**: Identifies a significant historical event that occurred on the current month and day according to the user's local time.
* **Daily Quiz**: Creates trivia questions of varying difficulties, including incorrect options and the latitude/longitude coordinates for the correct answer's location.

## Core Files

The core files for this integration are located within the directory `app/src/main/java/com.meta.pixelandtexel.geovoyage/services/llama` and its subfolders.

```
/services
    /llama
        QueryLlamaService.kt
        IQueryLlamaServiceHandler.kt


        /models
            BedrockRequest.kt
            BedrockResponse.kt
            OllamaRequest.kt
            OllamaResponse.kt
```

## Server options

This application supports two services for running the model and receiving results: [Ollama](https://ollama.com/) and [AWS Bedrock](https://aws.amazon.com/bedrock/).

The primary way to use the querying service in this application is through the `QueryLlamaService.submitQuery` function. You can access both server types via the single wrapper function shown below. The server type used is determined by the value stored in the application's SharedPreferences, which you can change via a toggle in the Settings menu. By default, it is set to AWS Bedrock.

```
fun submitQuery(
    query: String,
    creativity: Float = .6f, // temperature
    diversity: Float = .9f,  // top_p
    handler: IQueryLlamaServiceHandler
) {
    if(queryTemplate.isNullOrEmpty()) {
        throw Exception("Llama query template not created")
    }


    val fullQuery = String.format(queryTemplate!!, query)
    val temperature = creativity.clamp01()
    val top_p = diversity.clamp01()


    val serverType = SettingsService.get(
        KEY_LLAMA_SERVER_TYPE, LlamaServerType.AWS_BEDROCK.value)
    when (serverType) {
        LlamaServerType.OLLAMA.value -> queryOllama(
            fullQuery,
            temperature,
            top_p,
            handler
        )


        LlamaServerType.AWS_BEDROCK.value -> queryAWSBedrock(
            fullQuery,
            temperature,
            top_p,
            handler
        )
    }
}
```

**Note**: Both the `queryOllama` and `queryAWSBedrock` server functions use multithreading because they’re long-running operations that stream responses as the model generates them. Additionally, these implementations exclusively use the "generate" or "invoke" functionalities, although both APIs also support the LLM "chat" feature. This feature allows you to send follow-up queries that incorporate the previous dialog into the response generation. The choice of querying type should align with your specific use-case.


### Ollama

The Ollama model invocation uses a simple, unauthenticated HTTP request through the `/api/generate` endpoint, as detailed in the [official Ollama documentation](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion). You should configure the server URL in your `secrets.properties` file, but you can override it in the in-app Settings menu by selecting Ollama as your server type and entering the URL in the text field.

If you decide to use this server type for Llama invocation in a production application, it is highly recommended to add some form of authentication to your requests. An illustration of server-side authentication implementation was beyond the scope of this project, which serves as a proof-of-concept for integrating this service.

Ollama supports a number of [parameters](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values) for configuring your queries. For this application, only the parameters `temperature` and `top_p` were used to match the parameters that the AWS Bedrock model invocation SDK supports, which is more limited by comparison. The configuration of these parameters is explained in the Model Parameters section.

The Kotlin representation of the Ollama request payload is located in the file `app/src/main/java/com.meta.pixelandtexel.geovoyage/services/llama/models/OllamaRequest.kt`, and is serialized into JSON by the gson dependency before being set as the request body.

```
val jsonMediaType = "application/json; charset=utf-8".toMediaTypeOrNull()
val nativeRequest = OllamaRequest(query, OllamaRequestParams(temp, top_p))
val requestBody = gson.toJson(nativeRequest).toRequestBody(jsonMediaType)


val request = ollamaRequestBuilder.post(requestBody).build()
```

More information on the query construction can be found in the [Templated Queries](#templated-queries) section below.

### AWS Bedrock

The AWS Bedrock model invocation uses the [AWS Kotlin SDK](https://sdk.amazonaws.com/kotlin/api/latest/bedrockruntime/index.html) and requires access key and secret key authentication.

The AWS Kotlin SDK supports [three parameters](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-meta.html#model-parameters-meta-request-response) when invoking Meta's Llama model: temperature, top_p, and max_gen_length. The configuration of these parameters is detailed in the section titled [Model Parameters](#model-parameters).

The Kotlin representation of the AWS Bedrock request payload is located in the file `app/src/main/java/com.meta.pixelandtexel.geovoyage/services/llama/models/BedrockRequest.kt`, and it is also serialized into JSON by the gson dependency. Constructing the AWS Bedrock request payload is more complex than using Ollama, as it requires Llama 3's instruction format.

```
// Embed the prompt in Llama 3's instruction format.
val instruction = """
    <|begin_of_text|>
    <|start_header_id|>user<|end_header_id|>
    {{prompt}} <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
""".trimIndent().replace("{{prompt}}", query)


val nativeRequest = BedrockRequest(instruction, temp, top_p)
val requestBody = gson.toJson(nativeRequest)


val request = InvokeModelWithResponseStreamRequest {
    modelId = "meta.llama3-8b-instruct-v1:0"
    contentType = "application/json"
    accept = "application/json"
    body = requestBody.encodeToByteArray()
}
```

More information on the query construction can be found in the section below [Templated Queries](#templated-queries).

## Querying

Both Llama server types support a range of functionalities and options that let you configure the nature of the response when invoking models. The three most important techniques considered for this application are [model parameters](#model-parameters), [templated queries](#templated-queries), and [response streaming](#response-streaming).

### Model parameters

Only two parameters are actively utilized in the model invocation within this application: **temperature** and **top_p**. Although the system technically supports parameters to set the maximum number of tokens for the generated response, these are maintained at default values specific to each server type integration—128 for Ollama and 512 for AWS Bedrock.

A detailed discussion of these parameters and their impact on query responses is beyond the scope of this document, but here is a brief overview:

* **Temperature:** This parameter controls the creativity level of the model. A low value of 0.1 ensures minimal randomness and higher predictability.

* **Top_p:** This parameter determines the diversity level of the model. A default high value of 0.9 was selected to enhance the diversity of the responses.

Selecting the appropriate model invocation parameters depends on your specific use case. The values chosen for this application were determined after extensive testing to achieve a balance between educational value and engaging content.


### Templated queries

This app uses the "templated queries" technique, where variables or data are injected into pre-defined queries. There are 3 query templates defined below:

* **explorescreenbase_query**: In the Explore play mode, geocoordinates formatted in common notation (E/W and N/S instead of +/- to denote hemisphere) are injected at token 1, and the place name returned from the Google Geocoding API (if found) is injected at token 2. For more information regarding the usage of the Google Geocoding API, see [Geocoding API Overview](https://developers.google.com/maps/documentation/geocoding/overview).

    For example, "What is one notable city or landmark near the coordinates 37.4°N, 139.76°E in Japan?"

* **today_in_history_base_query**: In the Today in History play mode, the user's local date is injected at token 1 in the format of MMMM d.

    For example, "What is one notable event in history that occurred on August 30?"

* **base_query_template**: Lastly, all queries are injected into the base query, which is templated in the QueryLlamaService.submitQuery function just before being sent to the designated model server. This query accomplishes two tasks: ensuring the result isn't too long (preventing overflow in the allocated panel area and eliminating the need for the user to scroll), and transforming the response into Markdown format. All Llama text responses are displayed inside of the MarkdownText composable function available through the compose-markdown dependency. This method is a slightly unconventional, yet effective way to display a nicely formatted response from Llama in the application.

    For example, a user question: "In a short response formatted with markdown, answer the following question: Where are the tallest mountains on Earth?"

    For example, a Today in History query: "In a short response formatted with markdown, answer the following question: What is one notable event in history that occurred on August 30?"

The wording of templated queries significantly influences the content of the responses returned from model invocation, and extensive testing and tweaking were conducted to find the best wording for this application's purposes. For your own purposes, it is recommended that you dedicate time in your development to test and refine your templated queries if you choose to use this strategy.


### Response streaming

Integrating the Llama model invocation in this application utilizes response streaming to enhance user experience. Both Llama server types support non-streaming requests. However, using streaming minimizes waiting time for invocation completion and provides progressive visual feedback, keeping the user engaged. In most cases where you display text responses to the user, we recommend adopting this approach.


## Example usage

```
val fullQuery = String.format(templateQuery, data)


QueryLlamaService.submitQuery(
    query = fullQuery,
    creativity = 1f,
    diversity = .9f,
    handler = object : IQueryLlamaServiceHandler {
        override fun onStreamStart() {
            // (optional) hide loading message/graphic
        }


        override fun onPartial(partial: String) {
            // (optional) update result UI with partial response
        }


        override fun onFinished(answer: String) {
            // update result UI with full, final response
        }


        override fun onError(reason: String) {
            // handle querying error
        }
    }
)
```

## Pre-generated data

In addition to the queries executed during runtime, Llama 3 was used to generate educational data for users displayed in different play modes:

* **Daily quiz**: The questions and answers for this mode were generated with the following instructions:

    Generate 100 trivia questions related to Earth geography and cultures, ranked from easy to difficult, including the latitude and longitude coordinates of each location answer. Format the response in XML and provide two incorrect answers for each question.

* **Explore**: Landmark descriptions for this mode were generated with the following instructions:

    Provide short descriptions for each of the following landmarks: the Great Egyptian Pyramids, the Eiffel Tower, Chichén Itzá, the Sydney Opera House, Taj Mahal, the Christ the Redeemer statue, the Colosseum, Mount Vinson, and Victoria Falls. Format the responses in XML, including the name, description, latitude, and longitude of each landmark.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/geo-voyage-transport-users.md
---
title: Transport users to VR with Google Maps API
description: Learn how the Geo Voyage showcase uses the Google Maps API to create panoramic views of locations in VR.
last_updated: 2024-09-20
---

This application uses 2 APIs from the [Google Cloud Platform](https://console.cloud.google.com/) to fetch and display data and imagery about real world locations which correspond to points that users select on the globe.

* **Geocoding API**: Fetches information about a location on the globe.
* **Map Tiles API**: Fetches street view panoramic imagery from a location on the globe.

## Core Files

The core files for this integration are located within the directory `app/src/main/java/com/meta/pixelandtexel/geovoyage/services/googlemaps` and its subfolders.

```
/services
    /googlemaps
        GoogleMapsService.kt
        GoogleTilesService.kt
        IGeocodeServiceHandler.kt
        IPanoramaServiceHandler.kt

        /enums
            GeocodeStatus.kt

        /models
            GeocodeAddressComponent.kt
            GeocodePlusCode.kt
            GeocodeResponse.kt
            GeocodeResult.kt
            GoogleLocation.kt
            SessionRequest.kt
            SessionResponse.kt
```

## Reverse geocoding

Reverse geocoding, as described in the [official API documentation](https://developers.google.com/maps/documentation/geocoding/requests-reverse-geocoding), involves translating a map location into a human-readable address. In the Explore play mode of this application, the reverse geocoding service activates when a user drops a pin on the map. The application uses the address or location information returned from the API request to send a more informed query to the Llama server. For additional details on the templated Llama queries used in this application, refer to the relevant documentation page.

The service also functions as a validation or filtering mechanism. It excludes locations without known information or data on the Google Maps platform, such as areas in the middle of the Pacific Ocean, from being included in a Llama query.

The primary method for utilizing this reverse geocoding service in the application is through the `GoogleMapsService.getPlace` function. This function requires two arguments: a `GeoCoordinates` instance and an `IGeocodeServiceHandler` instance. The latter handles callbacks from the service and manages the events and results. The `getPlace` function operates as follows:

* Builds the request URL using the formatted geocoordinates as query parameters.
* Returns early if no results are found.
* Iterates through the results and extracts a name for the first place returned.

Note that in this application, the reverse geocode results are filtered by the place types included in the `resultTypeFilter` array below. The function succeeds and returns the `formatted_address` or `long_name` of the result, provided that at least one place of the specified types is returned from the API.

```
private val resultTypeFilter =
    listOf("country", "political", "natural_feature", "point_of_interest")
```

Unlike other services used by this application, which involve long-running operations, this service uses Kotlin coroutines to facilitate asynchronous execution for quick API calls.

### Example usage

You can see an example of usage in the `startQueryAtCoordinates` function located in the `/app/src/main/java/com/meta/pixelandtexel/geovoyage/viewmodels/ExploreViewModel.kt` file, where UI updates and error handling are implemented. It is important to handle errors gracefully and update the UI visible to the user appropriately.

```
GoogleMapsService.getPlace(coords, object : IGeocodeServiceHandler {
    override fun onFinished(place: String?) {
        if (place.isNullOrEmpty()) {
            // no location found; don't query llama
            return
        }

        // submit templated query to llama, with place name injected into query
    }

    override fun onError(reason: String) {
        // handle request error
    }
})
```

## Map tiles imagery for MR to VR transition

In the Explore play mode, when the user drops a pin on the globe, the [Google Maps Tiles API](https://developers.google.com/maps/documentation/tile) fetches metadata about panoramic images near that location. The API then displays the panorama in the headset using the [Street View Tiles](https://developers.google.com/maps/documentation/tile/streetview) endpoints.


### Methodology

This is the process used to display a panorama in-headset.

1. Create a new session that includes a token necessary for further API requests.
2. Fetch the metadata for a panoramic image closest to a set of geographical coordinates within a specified radius.
3. Determine the appropriate zoom level and image tiles needed to compose the full panoramic image.
4. Fetch the tiles as bitmaps.
5. Combine the bitmaps into a larger single bitmap.
6. Assign this bitmap image to a Spatial SDK skybox entity material.


### Getting the panorama image's metadata

The `GoogleTilesService.getPanoramaDataAt` function is where the application uses the Street View Tiles API. The function accepts a pair of geo coordinates and a search radius around those coordinates. The `streetview/metadata` endpoint then fetches the metadata for the panoramic image that’s closest to those coordinates and within the radius, provided such an image exists.

```
data class PanoMetadata(
    val panoId: String,

    // image and tile dimensions for fetching images to compose the full image

    val imageHeight: Int,
    val imageWidth: Int,
    val tileHeight: Int,
    val tileWidth: Int,

    // data about the image that Google requires you to display

    val copyright: String,
    val date: String?,
    val reportProblemLink: String,
)
```

Example usage:

```
val coords = GeoCoordinates(37.485073f, -122.150856f)
var panoData: PanoMetadata? = null

CoroutineScope(Dispatchers.Main).launch {
    panoData = GoogleTilesService.getPanoramaDataAt(coords, 10000)
}

if (panoData.value != null) {
    // display the metadata, and/or fetch and display the panorama bitmap
}
```

In this application, the API request occurs in the background when you drop a pin on the globe. If a panoramic image is available, the VR Mode button on the Explore panel becomes enabled. Selecting this enabled button triggers the next step in the implementation.

**Note**: The Map Tiles API [usage policy](https://developers.google.com/maps/documentation/tile/policies) requires you to display certain information when using their API in your application. In the PanoMetadata response, the last three properties appear on the Explore panel, as shown below. Selecting the **Report a problem with this image** link opens a web browser view to the specified URL.

![Report a problem with this image](/images/geo-user.png)

Next, you pass the fetched metadata to the `GoogleTilesService.getPanoramaBitmapFor` function. The function accepts the metadata object and an object that implements the `IPanoramaServiceHandler` interface to receive callbacks with the resulting Bitmap object or an error message.

```
interface IPanoramaServiceHandler {
    fun onFinished(bitmap: Bitmap)
    fun onError(reason: String)
}
```

Example usage:

```
GoogleTilesService.getPanoramaBitmapFor(
    panoData,
    object : IPanoramaServiceHandler {
        override fun onFinished(bitmap: Bitmap) {
            // set the skybox entity's material albedo texture to the bitmap
        }

        override fun onError(reason: String) {
            // handle request error
        }
    }
)
```

## Determining the zoom level and tiles to fetch

The streetview/tiles endpoint cannot fetch a full-size street view panoramic image in a single request. Instead, you must perform a series of requests, specifying a zoom level and the x/y indices of the tile you are fetching, then stitch them together to create a combined bitmap image. Zoom levels range from 0 to 5 and determine the approximate field of view for the tile image you are fetching. A higher zoom level results in a larger combined image with greater visible detail, requiring more tile image network requests. Conversely, a lower zoom level results in a lower visible quality combined image when viewed in a 360 view, but requires fewer network requests.

In this application, to determine the desired zoom level, calculate the largest image you can load while keeping the number of network requests needed to fetch the entire image below the predefined threshold MAX_TILE_FETCHES_PER_PANO, defined in GoogleTilesService. This methodology helps control the overall size and visible detail of the image, while also managing the number of network requests you must wait to complete before viewing the panorama in the headset.

The steps to calculate that zoom level are as follows:

1. Calculate the number of tiles needed to fetch the full resolution panorama image using the image and tile width/height values in the metadata.
2. Determine the zoom level needed to fetch the full resolution panorama image by using the approximate [field of view values](https://developers.google.com/maps/documentation/tile/streetview#street_view_image_tiles) for each zoom level.
3. Working backwards from that full resolution zoom level, decrease the calculated zoom level until the number of network requests required to fetch all tiles composing the entire image at that zoom level is less than or equal to MAX_TILE_FETCHES_PER_PANO.

**Note**: The panoramic images available from this API come from two sources: Google and public user-generated content. Additionally, the panorama images can vary in size. This application accounts for those different sizes by using the size values in the metadata to determine how the image tiles are fetched and stitched together.


## Fetching and combine the tiles

After the zoom level has been determined, the service concurrently fetches all of the tile images using tile coordinates and the zoom level. This implementation uses [Kotlin Coroutines](https://kotlinlang.org/docs/coroutines-overview.html) and async/await to accomplish asynchronous execution, and the [OkHttp library](https://square.github.io/okhttp/) and `BitmapFactory.decodeStream` function to fetch and create the Bitmap objects.

```
val numTotalTiles: Int = numTilesX * numTilesY

Log.d(TAG, "Begin fetching $numTotalTiles image tiles at zoom $zoom")

// fetch all of the tiles

val tilesFetches = (0 until numTotalTiles).map { i ->
    val x = i % numTilesX
    val y = i / numTilesX
    async(Dispatchers.IO) {
        getTileImage(metadata.panoId, x, y, zoom)
    }
}
val tiles = tilesFetches.mapNotNull { it.await() }

if (tiles.size < numTilesX * numTilesY) {
    throw Exception("Failed to get all tile images")
}
```

After all of the tiles have been fetched, this implementation iterates through the list of tiles and copies their content to a combined Bitmap object.

```
val combinedBitmap =
    Bitmap.createBitmap(fullWidth, fullHeight, Bitmap.Config.ARGB_8888)
val canvas = Canvas(combinedBitmap)

var src: Rect
var dst: Rect
for (y in 0 until numTilesY) {
    for (x in 0 until numTilesX) {
        // calculate the right and bottom boundaries for partial tiles
        val rightEdge = minOf((x + 1) * tileWidth, fullWidth)
        val bottomEdge = minOf((y + 1) * tileHeight, fullHeight)

        // skip tiles outside the bounds of the combined bitmap
        if (x * tileWidth >= fullWidth || y * tileHeight >= fullHeight) {
            continue
        }

        val tileIdx = y * numTilesX + x
        val tile = tiles[tileIdx]

        // now calculate the source and destination rects, only drawing the visible portion
        dst = Rect(x * tileWidth, y * tileHeight, rightEdge, bottomEdge)
        src = Rect(0, 0, dst.width(), dst.height())

        Log.d(
            TAG,
            "draw src rect $src from tile[$tileIdx] to combined bitmap at dst rect $dst"
        )

        canvas.drawBitmap(tile, src, dst, null)
    }
}
```


## Displaying the panorama

With the combined Bitmap object now returned from the `GoogleTilesService` object, you can display the 360 degree panorama in the headset. To do so, set the Spatial SDK skybox Entity's mesh material albedo texture to the Bitmap, and use the Visible component to set the Entity to be visible.

```
skyboxEntity.setComponent(Visible(false))

GoogleTilesService.getPanoramaBitmapFor(
    panoData,
    object : IPanoramaServiceHandler {
        override fun onFinished(bitmap: Bitmap) {
            if (!skyboxEntity.hasComponent<Mesh>() ||
                !skyboxEntity.hasComponent<Material>()
            ) {
                // handle skybox entity missing mesh or material
                return
            }

            val sceneMaterial = skyboxSceneObject!!.mesh?.materials?.get(0)
            if (sceneMaterial == null) {
                // handle skybox scene object mesh material not found
                return
            }

            // destroy our old skybox texture
            sceneMaterial.texture?.destroy()

            // set our new texture
            val sceneTexture = SceneTexture(bitmap)
            sceneMaterial.setAlbedoTexture(sceneTexture)

            skyboxEntity.setComponent(Visible(true))
        }

        override fun onError(reason: String) {
            // handle panorama fetch error
        }
    }
)
```

In this application, the skybox entity is defined in the scene.xml file. The skybox entity isn’t  visible until the user drops a pin on the globe during the Explore play mode:

```
<ac:Entity id="@integer/skybox_id">
    <ac:com.meta.aether.toolkit.Mesh src="mesh://skybox" />
    <ac:com.meta.aether.toolkit.Material unlit="true" />
    <ac:com.meta.aether.toolkit.Transform />
    <ac:com.meta.aether.toolkit.Visible isVisible="false" />
</ac:Entity>
```

## Balancing cost and quality

In addition to the number of network requests required to construct a 360 bitmap of the panorama, consider the cost implications when selecting a zoom/quality level for your application. Each tile image request incurs a [cost](https://developers.google.com/maps/billing-and-pricing/pricing#streetview), which can accumulate quickly when viewing many high-resolution panoramas. Moreover, each Google project has a [daily quota](https://developers.google.com/maps/documentation/tile/usage-and-billing#other-usage-limits) for the maximum number of image tile requests. Exceeding this limit will render the API inaccessible for the remainder of the day. For this application, a relatively high threshold for the number of network requests was established to fetch higher-resolution images, albeit at an increased cost.

Although it is out-of-scope for this application, employing a technique to fetch higher zoom level images in the direction the user is facing could reduce costs. The metadata for each panorama includes the heading, tilt, and roll information. If your application is designed for a headset, you could feasibly fetch higher quality images within the virtual camera's field of view and lower quality images outside of it. When the user turns their head, recalculate the tiles within the field of view and replace any lower resolution tiles with higher resolution ones. You can observe this technique in action by opening a panorama image in street view on [google.com/maps](https://www.google.com/maps/) and quickly panning the camera left or right.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/horizon-billing-compatibility
---
title: API Reference (1.0.0)
---

## root

### Packages

| Name |
|---|
| [com.meta.horizon.billingclient.api](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/) |
---
title: API Reference (1.1.0)
---

## root

### Packages

| Name |
|---|
| [com.meta.horizon.billingclient.api](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/) |
---
title: com.meta.horizon.billingclient.api
---

## Package-level declarations

### Types

| Name | Summary |
|---|---|
| [AccountIdentifiers](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/account-identifiers/) | data class [AccountIdentifiers](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/account-identifiers/)(val obfuscatedAccountId: String, val obfuscatedProfileId: String)<br>Account identifiers that were specified when the purchase was made. |
| [AcknowledgePurchaseParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/) | data class [AcknowledgePurchaseParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/)(val purchaseToken: String)<br>Parameters to acknowledge a purchase. See BillingClient.acknowledgePurchase. |
| [AcknowledgePurchaseResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-response-listener/) | interface [AcknowledgePurchaseResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-response-listener/)<br>Listener for the result of an acknowledge purchase request. |
| [AgeCategoryResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/age-category-response-listener/) | interface [AgeCategoryResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/age-category-response-listener/)<br>Listener to Age Category Response. |
| [AlternativeBillingListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-billing-listener/) | interface [~~AlternativeBillingListener~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-billing-listener/)<br>Listener interface for the developer-managed alternative billing flow, when it is chosen by the user when initiating a purchase. |
| [AlternativeBillingOnlyAvailabilityListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-availability-listener/) | interface [AlternativeBillingOnlyAvailabilityListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-availability-listener/)<br>Listener for the result of the isAlternativeBillingOnlyAvailableAsync API. |
| [AlternativeBillingOnlyInformationDialogListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-information-dialog-listener/) | interface [AlternativeBillingOnlyInformationDialogListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-information-dialog-listener/)<br>Listener for the result of the showAlternativeBillingOnlyInformationDialog API. |
| [AlternativeBillingOnlyReportingDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-reporting-details/) | data class [AlternativeBillingOnlyReportingDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-reporting-details/)(val externalTransactionToken: String)<br>This class is not used by Meta because Alternative Billing for IAP is not supported. |
| [AlternativeBillingOnlyReportingDetailsListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-reporting-details-listener/) | interface [AlternativeBillingOnlyReportingDetailsListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-reporting-details-listener/)<br>Listener for the result of the createAlternativeBillingOnlyReportingDetailsAsync API. |
| [AlternativeChoiceDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/) | data class [~~AlternativeChoiceDetails~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/)(val externalTransactionToken: String, val originalExternalTransactionId: String, val products: List&lt;[AlternativeChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/product/)&gt;)<br>Details related to a user's choice of alternative billing. |
| [BillingClient](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/) | abstract class [BillingClient](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/)<br>Main interface for communication between the library and user application code. |
| [BillingClientStateListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client-state-listener/) | interface [BillingClientStateListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client-state-listener/)<br>Callback for setup process. This listener's BillingClient.onBillingSetupFinished method is called when the setup process is complete. |
| [BillingConfig](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-config/) | data class [BillingConfig](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-config/)(val countryCode: String)<br>BillingConfig stores configuration used to perform billing operations. |
| [BillingConfigResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-config-response-listener/) | interface [BillingConfigResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-config-response-listener/)<br>Listener for the result of the getBillingConfigAsync API. |
| [BillingFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/) | data class [BillingFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/)(val obfuscatedAccountId: String? = null, val obfuscatedProfileId: String? = null, val isOfferPersonalized: Boolean = false, val productDetailsParamsList: List&lt;[BillingFlowParams.ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/)&gt; = emptyList(), val subscriptionUpdateParams: [BillingFlowParams.SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/)? = null, val skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/)? = null)<br>Parameters to initiate a purchase flow. See BillingClient.launchBillingFlow. |
| [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/) | data class [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/)(val responseCode: Int, val debugMessage: String)<br>Params containing the response code and the debug message from In-app Billing API response. |
| [ConsumeParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/consume-params/) | data class [ConsumeParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/consume-params/)(val purchaseToken: String)<br>Parameters to consume a purchase. See BillingClient.consumeAsync. |
| [ConsumeResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/consume-response-listener/) | interface [ConsumeResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/consume-response-listener/)<br>Callback that notifies when a consumption operation finishes. |
| [ExternalOfferAvailabilityListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/external-offer-availability-listener/) | interface [ExternalOfferAvailabilityListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/external-offer-availability-listener/)<br>Listener for the result of the isExternalOfferAvailableAsync API. |
| [ExternalOfferInformationDialogListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/external-offer-information-dialog-listener/) | interface [ExternalOfferInformationDialogListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/external-offer-information-dialog-listener/)<br>Listener for the result of the [BillingClient.showExternalOfferInformationDialog] API. |
| [ExternalOfferReportingDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/external-offer-reporting-details/) | data class [ExternalOfferReportingDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/external-offer-reporting-details/)(val externalTransactionToken: String)<br>The details used to report transactions made via external offer. |
| [ExternalOfferReportingDetailsListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/external-offer-reporting-details-listener/) | interface [ExternalOfferReportingDetailsListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/external-offer-reporting-details-listener/)<br>Listener for the result of the createExternalOfferReportingDetailsAsync API. |
| [GetBillingConfigParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/) | class [GetBillingConfigParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/)<br>Parameters for get billing config flow BillingClient.getBillingConfigAsync. |
| [InAppMessageParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-params/) | class [InAppMessageParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-params/)(inAppMessageCategoriesSet: Set&lt;Int&gt;)<br>Parameters for in-app messaging. See BillingClient.showInAppMessages. |
| [InAppMessageResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-response-listener/) | interface [InAppMessageResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-response-listener/)<br>Listener for the result of the in-app messaging flow. |
| [InAppMessageResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-result/) | data class [InAppMessageResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-result/)(val purchaseToken: String, val responseCode: Int)<br>Results related to in-app messaging. |
| [PendingPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/) | class [PendingPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/)<br>Parameters to enable pending purchases. |
| [PriceChangeConfirmationListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/price-change-confirmation-listener/) | interface [~~PriceChangeConfirmationListener~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/price-change-confirmation-listener/)<br>Listener to a result of the price change confirmation flow. |
| [PriceChangeFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/) | data class [~~PriceChangeFlowParams~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/)(val skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/))<br>Parameters to launch a price change confirmation flow. |
| [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/) | data class [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/)(val productId: String, val title: String = &quot;&quot;, val name: String = &quot;&quot;, val description: String = &quot;&quot;, val productType: String, val oneTimePurchaseOfferDetails: [ProductDetails.OneTimePurchaseOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/one-time-purchase-offer-details/)?, var subscriptionOfferDetails: List&lt;[ProductDetails.SubscriptionOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/subscription-offer-details/)&gt;?)<br>Represents the details of a one time or subscription product. |
| [ProductDetailsResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details-response-listener/) | interface [ProductDetailsResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details-response-listener/)<br>Listener to a result of product details query. |
| [Purchase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase/) | data class [Purchase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase/)(val purchaseTime: Long, val purchaseToken: String, val products: List&lt;String&gt;, val packageName: String, val developerPayload: String? = &quot;&quot;, val orderId: String? = &quot;&quot;, val originalJson: String? = &quot;&quot;, val quantity: Int = 1, val signature: String = &quot;&quot;)<br>Represents an in-app billing purchase. |
| [PurchaseHistoryRecord](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase-history-record/) | data class [PurchaseHistoryRecord](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase-history-record/)(val purchaseTime: Long, val purchaseToken: String, val products: List&lt;String&gt;, val developerPayload: String? = &quot;&quot;, val originalJson: String? = &quot;&quot;, val quantity: Int = 1, val signature: String = &quot;&quot;)<br>Represents an in-app billing purchase history record. |
| [PurchaseHistoryResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase-history-response-listener/) | interface [PurchaseHistoryResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase-history-response-listener/)<br>Listener to a result of purchase history query. |
| [PurchasesResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchases-response-listener/) | interface [PurchasesResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchases-response-listener/)<br>Listener to a result of purchases query. |
| [PurchasesUpdatedListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchases-updated-listener/) | interface [PurchasesUpdatedListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchases-updated-listener/)<br>Listener interface for purchase updates which happen when, for example, the user buys something within the app or by initiating a purchase from the Store. |
| [QueryProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/) | data class [QueryProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/)(val productList: List&lt;[QueryProductDetailsParams.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)&gt;)<br>Parameters to initiate a query for Product details BillingClient.queryProductDetailsAsync. |
| [QueryPurchaseHistoryParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/) | data class [QueryPurchaseHistoryParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/)(val productType: String)<br>Parameters to initiate a query for purchase history. |
| [QueryPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchases-params/) | data class [QueryPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchases-params/)(val productType: String)<br>Parameters to initiate a query for purchases. |
| [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/) | data class [~~SkuDetails~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/)(val price: String, val priceAmountMicros: Long, val priceCurrencyCode: String, val sku: String, val subscriptionPeriod: String, val title: String, val description: String, val type: String, val originalPrice: String = &quot;&quot;, val originalPriceAmountMicros: Long = 0, val originalJson: String = &quot;&quot;, val introductoryPrice: String = &quot;&quot;, val introductoryPriceAmountMicros: Long = 0, val introductoryPriceCycles: Int = 0, val introductoryPricePeriod: String = &quot;&quot;, val iconUrl: String = &quot;&quot;, val freeTrialPeriod: String = &quot;&quot;)<br>Represents an in-app product's or subscription's listing details. |
| [SkuDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details-params/) | data class [~~SkuDetailsParams~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details-params/)(val skuType: String, val skusList: List&lt;String&gt;)<br>Parameters to initiate a query for SKU details. See BillingClient.querySkuDetailsAsync. |
| [SkuDetailsResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details-response-listener/) | interface [~~SkuDetailsResponseListener~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details-response-listener/)<br>Listener to a result of SKU details query. |
| [UserChoiceBillingListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/user-choice-billing-listener/) | interface [UserChoiceBillingListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/user-choice-billing-listener/)<br>Listener interface for the developer-managed alternative billing flow, when it is chosen by the user when initiating a purchase. |
| [UserChoiceDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/user-choice-details/) | data class [UserChoiceDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/user-choice-details/)(val externalTransactionId: String, val originalExternalTransactionId: String, val products: List&lt;[UserChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/)&gt;)<br>Details related to a user's choice of alternative billing. |
---
title: PurchaseHistoryResponseListener
---

## PurchaseHistoryResponseListener

interface PurchaseHistoryResponseListener

Listener to a result of purchase history query. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for PurchaseHistoryResponseListener](https://developer.android.com/reference/com/android/billingclient/api/PurchaseHistoryResponseListener).

### Functions

| Name | Summary |
|---|---|
| onPurchaseHistoryResponse | abstract fun onPurchaseHistoryResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/), purchaseHistoryRecordList: List&lt;[PurchaseHistoryRecord](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase-history-record/)&gt;)<br>Called to notify that the query purchase history operation has finished. |
---
title: SkuDetails
---

## SkuDetails

data class ~~SkuDetails~~(val price: String, val priceAmountMicros: Long, val priceCurrencyCode: String, val sku: String, val subscriptionPeriod: String, val title: String, val description: String, val type: String, val originalPrice: String = &quot;&quot;, val originalPriceAmountMicros: Long = 0, val originalJson: String = &quot;&quot;, val introductoryPrice: String = &quot;&quot;, val introductoryPriceAmountMicros: Long = 0, val introductoryPriceCycles: Int = 0, val introductoryPricePeriod: String = &quot;&quot;, val iconUrl: String = &quot;&quot;, val freeTrialPeriod: String = &quot;&quot;)

#### Deprecated

This class is deprecated. Use [BillingClient.queryProductDetailsAsync] instead.

---

Represents an in-app product's or subscription's listing details.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for SkuDetails](https://developer.android.com/reference/com/android/billingclient/api/SkuDetails).

### Constructors

| Name | Summary |
|---|---|
| SkuDetails | constructor(ovrProduct: &lt;Error class: unknown class&gt;)constructor(originalJson: String)constructor(price: String, priceAmountMicros: Long, priceCurrencyCode: String, sku: String, subscriptionPeriod: String, title: String, description: String, type: String, originalPrice: String = &quot;&quot;, originalPriceAmountMicros: Long = 0, originalJson: String = &quot;&quot;, introductoryPrice: String = &quot;&quot;, introductoryPriceAmountMicros: Long = 0, introductoryPriceCycles: Int = 0, introductoryPricePeriod: String = &quot;&quot;, iconUrl: String = &quot;&quot;, freeTrialPeriod: String = &quot;&quot;) |

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| description | val description: String<br>Returns the description of the product. |
| freeTrialPeriod | val freeTrialPeriod: String<br>Trial period configured in the Developer Dashboard, specified in ISO 8601 format. For example, P7D equates to seven days. To learn more about free trial eligibility, see In-app Subscriptions. |
| iconUrl | val iconUrl: String<br>Returns the icon of the product if present. |
| introductoryPrice | val introductoryPrice: String<br>Formatted introductory price of a subscription, including its currency sign, such as €3.99. For tax exclusive countries, the price doesn't include tax. |
| introductoryPriceAmountMicros | val introductoryPriceAmountMicros: Long = 0<br>Introductory price in micro-units. The currency is the same as price_currency_code. |
| introductoryPriceCycles | val introductoryPriceCycles: Int = 0<br>The number of subscription billing periods for which the user will be given the introductory price, such as 3. |
| introductoryPricePeriod | val introductoryPricePeriod: String<br>The billing period of the introductory price, specified in ISO 8601 format. |
| originalJson | val originalJson: String<br>Returns a String in JSON format that contains SKU details. |
| originalPrice | val originalPrice: String<br>Returns formatted original price of the item, including its currency sign. |
| originalPriceAmountMicros | val originalPriceAmountMicros: Long = 0<br>Returns the original price in micro-units, where 1,000,000 micro-units equal one unit of the currency. |
| price | val price: String<br>Returns formatted price of the item, including its currency sign. |
| priceAmountMicros | val priceAmountMicros: Long<br>Returns price in micro-units, where 1,000,000 micro-units equal one unit of the currency. |
| priceCurrencyCode | val priceCurrencyCode: String<br>Returns ISO 4217 currency code for price and original price. |
| sku | val sku: String<br>Returns the product Id. |
| subscriptionPeriod | val subscriptionPeriod: String<br>Subscription period, specified in ISO 8601 format. For example, P1W equates to one week, P1M equates to one month, P3M equates to three months, P6M equates to six months, and P1Y equates to one year. |
| title | val title: String<br>Returns the title of the product being sold. |
| type | val type: String<br>Returns the {@link BillingClient.SkuType} of the SKU. |

## Companion

object Companion
---
title: UserChoiceBillingListener
---

## UserChoiceBillingListener

interface UserChoiceBillingListener

Listener interface for the developer-managed alternative billing flow, when it is chosen by the user when initiating a purchase. 

Alternative Billing for IAP is not supported by Meta. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for UserChoiceBillingListener](https://developer.android.com/reference/com/android/billingclient/api/UserChoiceBillingListener).

### Functions

| Name | Summary |
|---|---|
| userSelectedAlternativeBilling | abstract fun userSelectedAlternativeBilling(userChoiceDetails: [UserChoiceDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/user-choice-details/))<br>Called when a user has selected to make a purchase using user choice billing. |
---
title: SkuDetailsParams
---

## SkuDetailsParams

data class ~~SkuDetailsParams~~(val skuType: String, val skusList: List&lt;String&gt;)

#### Deprecated

Use [BillingClient.queryProductDetailsAsync] instead

---

Parameters to initiate a query for SKU details. See BillingClient.querySkuDetailsAsync.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for SkuDetailsParams](https://developer.android.com/reference/com/android/billingclient/api/SkuDetailsParams).

### Constructors

| Name | Summary |
|---|---|
| SkuDetailsParams | constructor(skuType: String, skusList: List&lt;String&gt;) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details-params/builder/) |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| skusList | val skusList: List&lt;String&gt;<br>The list of SKUs to query. |
| skuType | val skuType: String<br>The SkuType of the SKUs to query. |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [SkuDetailsParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) |
---
title: QueryPurchasesParams
---

## QueryPurchasesParams

data class QueryPurchasesParams(val productType: String)

Parameters to initiate a query for purchases.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for QueryPurchasesParams](https://developer.android.com/reference/com/android/billingclient/api/QueryPurchasesParams).

### Constructors

| Name | Summary |
|---|---|
| QueryPurchasesParams | constructor(productType: String) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchases-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchases-params/builder/) |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| productType | val productType: String |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [QueryPurchasesParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/)<br>Constructs a new [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) instance. |
---
title: com.meta.horizon.billingclient.api
last_updated: 2025-03-19
---

## Package-level declarations

### Types

| Name | Summary |
|---|---|
| [AccountIdentifiers](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/account-identifiers/) | data class [AccountIdentifiers](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/account-identifiers/)(val obfuscatedAccountId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val obfuscatedProfileId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>Account identifiers that were specified when the purchase was made. |
| [AcknowledgePurchaseParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/) | data class [AcknowledgePurchaseParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/)(val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>Parameters to acknowledge a purchase. See BillingClient.acknowledgePurchase. |
| [AcknowledgePurchaseResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-response-listener/) | interface [AcknowledgePurchaseResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-response-listener/)<br>Listener for the result of an acknowledge purchase request. |
| [AgeCategoryResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/age-category-response-listener/) | interface [AgeCategoryResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/age-category-response-listener/)<br>Listener to Age Category Response. |
| [AlternativeBillingListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-billing-listener/) | interface [~~AlternativeBillingListener~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-billing-listener/)<br>Listener interface for the developer-managed alternative billing flow, when it is chosen by the user when initiating a purchase. |
| [AlternativeBillingOnlyAvailabilityListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-availability-listener/) | interface [AlternativeBillingOnlyAvailabilityListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-availability-listener/)<br>Listener for the result of the isAlternativeBillingOnlyAvailableAsync API. |
| [AlternativeBillingOnlyInformationDialogListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-information-dialog-listener/) | interface [AlternativeBillingOnlyInformationDialogListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-information-dialog-listener/)<br>Listener for the result of the showAlternativeBillingOnlyInformationDialog API. |
| [AlternativeBillingOnlyReportingDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-reporting-details/) | data class [AlternativeBillingOnlyReportingDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-reporting-details/)(val externalTransactionToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>This class is not used by Meta because Alternative Billing for IAP is not supported. |
| [AlternativeBillingOnlyReportingDetailsListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-reporting-details-listener/) | interface [AlternativeBillingOnlyReportingDetailsListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-reporting-details-listener/)<br>Listener for the result of the createAlternativeBillingOnlyReportingDetailsAsync API. |
| [AlternativeChoiceDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/) | data class [~~AlternativeChoiceDetails~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/)(val externalTransactionToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val originalExternalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[AlternativeChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/product/)&gt;)<br>Details related to a user's choice of alternative billing. |
| [BillingClient](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/) | abstract class [BillingClient](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/)<br>Main interface for communication between the library and user application code. |
| [BillingClientStateListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client-state-listener/) | interface [BillingClientStateListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client-state-listener/)<br>Callback for setup process. This listener's BillingClient.onBillingSetupFinished method is called when the setup process is complete. |
| [BillingConfig](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-config/) | data class [BillingConfig](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-config/)(val countryCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>BillingConfig stores configuration used to perform billing operations. |
| [BillingConfigResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-config-response-listener/) | interface [BillingConfigResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-config-response-listener/)<br>Listener for the result of the getBillingConfigAsync API. |
| [BillingFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/) | data class [BillingFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/)(val obfuscatedAccountId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null, val obfuscatedProfileId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null, val isOfferPersonalized: [Boolean](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/boolean/index.html) = false, val productDetailsParamsList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[BillingFlowParams.ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/)&gt; = emptyList(), val subscriptionUpdateParams: [BillingFlowParams.SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/)? = null, val skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/)? = null)<br>Parameters to initiate a purchase flow. See BillingClient.launchBillingFlow. |
| [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/) | data class [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/)(val responseCode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html), val debugMessage: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>Params containing the response code and the debug message from In-app Billing API response. |
| [ConsumeParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/consume-params/) | data class [ConsumeParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/consume-params/)(val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>Parameters to consume a purchase. See BillingClient.consumeAsync. |
| [ConsumeResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/consume-response-listener/) | interface [ConsumeResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/consume-response-listener/)<br>Callback that notifies when a consumption operation finishes. |
| [ExternalOfferAvailabilityListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/external-offer-availability-listener/) | interface [ExternalOfferAvailabilityListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/external-offer-availability-listener/)<br>Listener for the result of the isExternalOfferAvailableAsync API. |
| [ExternalOfferInformationDialogListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/external-offer-information-dialog-listener/) | interface [ExternalOfferInformationDialogListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/external-offer-information-dialog-listener/)<br>Listener for the result of the [BillingClient.showExternalOfferInformationDialog] API. |
| [ExternalOfferReportingDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/external-offer-reporting-details/) | data class [ExternalOfferReportingDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/external-offer-reporting-details/)(val externalTransactionToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>The details used to report transactions made via external offer. |
| [ExternalOfferReportingDetailsListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/external-offer-reporting-details-listener/) | interface [ExternalOfferReportingDetailsListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/external-offer-reporting-details-listener/)<br>Listener for the result of the createExternalOfferReportingDetailsAsync API. |
| [GetBillingConfigParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/) | class [GetBillingConfigParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/)<br>Parameters for get billing config flow BillingClient.getBillingConfigAsync. |
| [InAppMessageParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-params/) | class [InAppMessageParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-params/)(inAppMessageCategoriesSet: [Set](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/set/index.html)&lt;[Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)&gt;)<br>Parameters for in-app messaging. See BillingClient.showInAppMessages. |
| [InAppMessageResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-response-listener/) | interface [InAppMessageResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-response-listener/)<br>Listener for the result of the in-app messaging flow. |
| [InAppMessageResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-result/) | data class [InAppMessageResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-result/)(val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val responseCode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html))<br>Results related to in-app messaging. |
| [PendingPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/) | class [PendingPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/)<br>Parameters to enable pending purchases. |
| [PriceChangeConfirmationListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/price-change-confirmation-listener/) | interface [~~PriceChangeConfirmationListener~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/price-change-confirmation-listener/)<br>Listener to a result of the price change confirmation flow. |
| [PriceChangeFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/) | data class [~~PriceChangeFlowParams~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/)(val skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/))<br>Parameters to launch a price change confirmation flow. |
| [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/) | data class [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/)(val productId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val title: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val name: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val description: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val oneTimePurchaseOfferDetails: [ProductDetails.OneTimePurchaseOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/one-time-purchase-offer-details/)?, var subscriptionOfferDetails: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[ProductDetails.SubscriptionOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/subscription-offer-details/)&gt;?)<br>Represents the details of a one time or subscription product. |
| [ProductDetailsResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details-response-listener/) | interface [ProductDetailsResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details-response-listener/)<br>Listener to a result of product details query. |
| [Purchase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase/) | data class [Purchase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase/)(val purchaseTime: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;, val packageName: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val developerPayload: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, val orderId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, val originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, val quantity: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1, val signature: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;)<br>Represents an in-app billing purchase. |
| [PurchaseHistoryRecord](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase-history-record/) | data class [PurchaseHistoryRecord](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase-history-record/)(val purchaseTime: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;, val developerPayload: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, val originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, val quantity: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1, val signature: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;)<br>Represents an in-app billing purchase history record. |
| [PurchaseHistoryResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase-history-response-listener/) | interface [PurchaseHistoryResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase-history-response-listener/)<br>Listener to a result of purchase history query. |
| [PurchasesResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchases-response-listener/) | interface [PurchasesResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchases-response-listener/)<br>Listener to a result of purchases query. |
| [PurchasesUpdatedListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchases-updated-listener/) | interface [PurchasesUpdatedListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchases-updated-listener/)<br>Listener interface for purchase updates which happen when, for example, the user buys something within the app or by initiating a purchase from the Store. |
| [QueryProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/) | data class [QueryProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/)(val productList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[QueryProductDetailsParams.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)&gt;)<br>Parameters to initiate a query for Product details BillingClient.queryProductDetailsAsync. |
| [QueryPurchaseHistoryParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/) | data class [QueryPurchaseHistoryParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/)(val productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>Parameters to initiate a query for purchase history. |
| [QueryPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchases-params/) | data class [QueryPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchases-params/)(val productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>Parameters to initiate a query for purchases. |
| [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/) | data class [~~SkuDetails~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/)(val price: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val priceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), val priceCurrencyCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val sku: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val subscriptionPeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val title: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val description: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val originalPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val originalPriceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html) = 0, val originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val introductoryPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val introductoryPriceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html) = 0, val introductoryPriceCycles: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 0, val introductoryPricePeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val iconUrl: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val freeTrialPeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;)<br>Represents an in-app product's or subscription's listing details. |
| [SkuDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details-params/) | data class [~~SkuDetailsParams~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details-params/)(val skuType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val skusList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;)<br>Parameters to initiate a query for SKU details. See BillingClient.querySkuDetailsAsync. |
| [SkuDetailsResponseListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details-response-listener/) | interface [~~SkuDetailsResponseListener~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details-response-listener/)<br>Listener to a result of SKU details query. |
| [UserChoiceBillingListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/user-choice-billing-listener/) | interface [UserChoiceBillingListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/user-choice-billing-listener/)<br>Listener interface for the developer-managed alternative billing flow, when it is chosen by the user when initiating a purchase. |
| [UserChoiceDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/user-choice-details/) | data class [UserChoiceDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/user-choice-details/)(val externalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val originalExternalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[UserChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/)&gt;)<br>Details related to a user's choice of alternative billing. |
---
title: SkuDetailsResponseListener
---

## SkuDetailsResponseListener

interface ~~SkuDetailsResponseListener~~

#### Deprecated

---

Listener to a result of SKU details query. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for SkuDetailsResponseListener](https://developer.android.com/reference/com/android/billingclient/api/SkuDetailsResponseListener).

##### Deprecated

Use queryProductDetailsAsync instead.

### Functions

| Name | Summary |
|---|---|
| onSkuDetailsResponse | abstract fun onSkuDetailsResponse(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/), skuDetails: List&lt;[SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/)&gt;)<br>Called to notify that a fetch SKU details operation has finished. |
---
title: UserChoiceDetails
---

## UserChoiceDetails

data class UserChoiceDetails(val externalTransactionId: String, val originalExternalTransactionId: String, val products: List&lt;[UserChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/)&gt;)

Details related to a user's choice of alternative billing.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for UserChoiceDetails](https://developer.android.com/reference/com/android/billingclient/api/UserChoiceDetails).

### Constructors

| Name | Summary |
|---|---|
| UserChoiceDetails | constructor(externalTransactionId: String, originalExternalTransactionId: String, products: List&lt;[UserChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/)&gt;) |

### Types

| Name | Summary |
|---|---|
| [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/) | data class [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/)(val id: String, val offerToken: String, val type: String) |

### Properties

| Name | Summary |
|---|---|
| externalTransactionId | val externalTransactionId: String<br>A token that represents the user's prospective purchase via user choice alternative billing. |
| originalExternalTransactionId | val originalExternalTransactionId: String<br>The external transaction Id of the originating subscription, if the purchase is a subscription upgrade/downgrade. |
| products | val products: List&lt;[UserChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/)&gt;<br>A list of [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/) to be purchased in the user choice alternative billing flow. |
---
title: QueryPurchaseHistoryParams
---

## QueryPurchaseHistoryParams

data class QueryPurchaseHistoryParams(val productType: String)

Parameters to initiate a query for purchase history.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for QueryPurchaseHistoryParams](https://developer.android.com/reference/com/android/billingclient/api/QueryPurchaseHistoryParams).

### Constructors

| Name | Summary |
|---|---|
| QueryPurchaseHistoryParams | constructor(productType: String) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/builder/) |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| productType | val productType: String |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [QueryPurchaseHistoryParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/)<br>Constructs a new [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) instance. |
---
title: AlternativeBillingOnlyInformationDialogListener
---

## AlternativeBillingOnlyInformationDialogListener

interface AlternativeBillingOnlyInformationDialogListener

Listener for the result of the showAlternativeBillingOnlyInformationDialog API. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for AlternativeBillingOnlyInformationDialogListener](https://developer.android.com/reference/com/android/billingclient/api/AlternativeBillingOnlyInformationDialogListener).

### Functions

| Name | Summary |
|---|---|
| onAlternativeBillingOnlyInformationDialogResponse | abstract fun onAlternativeBillingOnlyInformationDialogResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called to notify that the alternative billing only dialog flow is finished. |
---
title: AlternativeBillingOnlyReportingDetailsListener
---

## AlternativeBillingOnlyReportingDetailsListener

interface AlternativeBillingOnlyReportingDetailsListener

Listener for the result of the createAlternativeBillingOnlyReportingDetailsAsync API. 

Alternative Billing for IAP is not supported by Meta. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for AlternativeBillingOnlyReportingDetailsListener](https://developer.android.com/reference/com/android/billingclient/api/AlternativeBillingOnlyReportingDetailsListener).

### Functions

| Name | Summary |
|---|---|
| onAlternativeBillingOnlyTokenResponse | abstract fun onAlternativeBillingOnlyTokenResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/), alternativeBillingOnlyReportingDetails: [AlternativeBillingOnlyReportingDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-reporting-details/))<br>Called to receive the results from createAlternativeBillingOnlyReportingDetailsAsync when it is finished. |
---
title: BillingClientStateListener
---

## BillingClientStateListener

interface BillingClientStateListener

Callback for setup process. This listener's BillingClient.onBillingSetupFinished method is called when the setup process is complete.

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for BillingClientStateListener](https://developer.android.com/reference/com/android/billingclient/api/BillingClientStateListener).

### Functions

| Name | Summary |
|---|---|
| onBillingServiceDisconnected | abstract fun onBillingServiceDisconnected()<br>Called to notify that the connection to the billing service was lost. |
| onBillingSetupFinished | abstract fun onBillingSetupFinished(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called to notify that setup is complete. |
---
title: InAppMessageResponseListener
---

## InAppMessageResponseListener

interface InAppMessageResponseListener

Listener for the result of the in-app messaging flow. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for InAppMessageResponseListener](https://developer.android.com/reference/com/android/billingclient/api/InAppMessageResponseListener).

### Functions

| Name | Summary |
|---|---|
| onInAppMessageResponse | abstract fun onInAppMessageResponse(inAppMessageResult: [InAppMessageResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-result/))<br>Called to notify when the in-app messaging flow has finished. |
---
title: AlternativeChoiceDetails
---

## AlternativeChoiceDetails

data class ~~AlternativeChoiceDetails~~(val externalTransactionToken: String, val originalExternalTransactionId: String, val products: List&lt;[AlternativeChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/product/)&gt;)

#### Deprecated

Use [BillingClient.Builder.enableUserChoiceBilling] with [UserChoiceBillingListener] and [UserChoiceDetails] in the listener callback instead.

---

Details related to a user's choice of alternative billing.

Alternative Billing for IAP is not supported by Meta.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for AlternativeChoiceDetails](https://developer.android.com/reference/com/android/billingclient/api/AlternativeChoiceDetails).

### Constructors

| Name | Summary |
|---|---|
| AlternativeChoiceDetails | constructor(externalTransactionToken: String, originalExternalTransactionId: String, products: List&lt;[AlternativeChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/product/)&gt;) |

### Types

| Name | Summary |
|---|---|
| [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/product/) | data class [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/product/)(val id: String, val offerToken: String, val type: String)<br>Details about a product being purchased. |

### Properties

| Name | Summary |
|---|---|
| externalTransactionToken | val externalTransactionToken: String<br>A token that represents the user's prospective purchase via alternative billing. |
| originalExternalTransactionId | val originalExternalTransactionId: String<br>The external transaction Id of the originating subscription, if the purchase is a subscription upgrade/downgrade. |
| products | val products: List&lt;[AlternativeChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/product/)&gt;<br>A list of Product to be purchased in the alternative billing flow. |
---
title: AlternativeBillingOnlyReportingDetails
---

## AlternativeBillingOnlyReportingDetails

data class AlternativeBillingOnlyReportingDetails(val externalTransactionToken: String)

This class is not used by Meta because Alternative Billing for IAP is not supported.

The details used to report transactions made via alternative billing without user choice to use Google Play billing.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for AlternativeBillingOnlyReportingDetails](https://developer.android.com/reference/com/android/billingclient/api/AlternativeBillingOnlyReportingDetails).

### Constructors

| Name | Summary |
|---|---|
| AlternativeBillingOnlyReportingDetails | constructor(externalTransactionToken: String) |

### Properties

| Name | Summary |
|---|---|
| externalTransactionToken | val externalTransactionToken: String<br>An external transaction token that can be used to report a transaction made via alternative billing without user choice to use Google Play billing. |
---
title: QueryProductDetailsParams
---

## QueryProductDetailsParams

data class QueryProductDetailsParams(val productList: List&lt;[QueryProductDetailsParams.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)&gt;)

Parameters to initiate a query for Product details BillingClient.queryProductDetailsAsync.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for QueryProductDetailsParams](https://developer.android.com/reference/com/android/billingclient/api/QueryProductDetailsParams).

### Constructors

| Name | Summary |
|---|---|
| QueryProductDetailsParams | constructor(productList: List&lt;[QueryProductDetailsParams.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)&gt;) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/builder/) |
| Companion | object Companion |
| [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/) | data class [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)(val productId: String, val productType: String)<br>A Product identifier used for querying product details. |

### Properties

| Name | Summary |
|---|---|
| productList | val productList: List&lt;[QueryProductDetailsParams.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)&gt; |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [QueryProductDetailsParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/)<br>Constructs a new [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) instance. |
---
title: PurchasesUpdatedListener
---

## PurchasesUpdatedListener

interface PurchasesUpdatedListener

Listener interface for purchase updates which happen when, for example, the user buys something within the app or by initiating a purchase from the Store. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for PurchasesUpdatedListener](https://developer.android.com/reference/com/android/billingclient/api/PurchasesUpdatedListener).

### Functions

| Name | Summary |
|---|---|
| onPurchasesUpdated | abstract fun onPurchasesUpdated(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/), purchases: List&lt;[Purchase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase/)&gt;) |
---
title: PurchasesResponseListener
---

## PurchasesResponseListener

interface PurchasesResponseListener

Listener to a result of purchases query. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for PurchasesResponseListener](https://developer.android.com/reference/com/android/billingclient/api/PurchasesResponseListener).

### Functions

| Name | Summary |
|---|---|
| onQueryPurchasesResponse | abstract fun onQueryPurchasesResponse(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/), purchases: List&lt;[Purchase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase/)&gt;)<br>Called to notify that the query purchases operation has finished. |
---
title: PurchaseHistoryRecord
---

## PurchaseHistoryRecord

data class PurchaseHistoryRecord(val purchaseTime: Long, val purchaseToken: String, val products: List&lt;String&gt;, val developerPayload: String? = &quot;&quot;, val originalJson: String? = &quot;&quot;, val quantity: Int = 1, val signature: String = &quot;&quot;)

Represents an in-app billing purchase history record.

This class includes a subset of fields in [Purchase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase/).

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for PurchaseHistoryRecord](https://developer.android.com/reference/com/android/billingclient/api/PurchaseHistoryRecord).

### Constructors

| Name | Summary |
|---|---|
| PurchaseHistoryRecord | constructor(jsonPurchaseInfo: String, signature: String)constructor(purchaseTime: Long, purchaseToken: String, products: List&lt;String&gt;, developerPayload: String? = &quot;&quot;, originalJson: String? = &quot;&quot;, quantity: Int = 1, signature: String = &quot;&quot;) |

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| developerPayload | val developerPayload: String?<br>Returns the payload specified when the purchase was acknowledged or consumed. |
| originalJson | val originalJson: String?<br>Returns a String in JSON format that contains details about the purchase order. |
| products | val products: List&lt;String&gt;<br>Returns the product Ids. |
| purchaseTime | val purchaseTime: Long<br>Returns the time the product was purchased, in milliseconds since the epoch (Jan 1, 1970). |
| purchaseToken | val purchaseToken: String<br>Returns a token that uniquely identifies a purchase for a given item and user pair. |
| quantity | val quantity: Int = 1<br>Returns the quantity of the purchased product. |
| signature | val signature: String<br>String containing the signature of the purchase data that was signed with the private key of the developer. |

### Functions

| Name | Summary |
|---|---|
| getSkus | fun ~~getSkus~~(): &lt;Error class: unknown class&gt;&lt;String&gt;<br>Returns the product Ids. |

## Companion

object Companion
---
title: AlternativeBillingOnlyAvailabilityListener
---

## AlternativeBillingOnlyAvailabilityListener

interface AlternativeBillingOnlyAvailabilityListener

Listener for the result of the isAlternativeBillingOnlyAvailableAsync API. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for AlternativeBillingOnlyAvailabilityListener](https://developer.android.com/reference/com/android/billingclient/api/AlternativeBillingOnlyAvailabilityListener).

### Functions

| Name | Summary |
|---|---|
| onAlternativeBillingOnlyAvailabilityResponse | abstract fun onAlternativeBillingOnlyAvailabilityResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called when a user has selected to make a purchase using alternative billing. |
---
title: AccountIdentifiers
---

## AccountIdentifiers

data class AccountIdentifiers(val obfuscatedAccountId: String, val obfuscatedProfileId: String)

Account identifiers that were specified when the purchase was made.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for AccountIdentifiers](https://developer.android.com/reference/com/android/billingclient/api/AccountIdentifiers).

### Constructors

| Name | Summary |
|---|---|
| AccountIdentifiers | constructor(obfuscatedAccountId: String, obfuscatedProfileId: String) |

### Properties

| Name | Summary |
|---|---|
| obfuscatedAccountId | val obfuscatedAccountId: String<br>The obfuscated account id specified in BillingFlowParams.Builder.setObfuscatedAccountId. |
| obfuscatedProfileId | val obfuscatedProfileId: String<br>The obfuscated profile id specified in BillingFlowParams.Builder.setObfuscatedProfileId. |
---
title: AlternativeBillingListener
---

## AlternativeBillingListener

interface ~~AlternativeBillingListener~~

#### Deprecated

---

Listener interface for the developer-managed alternative billing flow, when it is chosen by the user when initiating a purchase. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for AlternativeBillingListener](https://developer.android.com/reference/com/android/billingclient/api/AlternativeBillingListener).

##### Deprecated

Use enableUserChoiceBilling with  instead.

### Functions

| Name | Summary |
|---|---|
| userSelectedAlternativeBilling | abstract fun userSelectedAlternativeBilling(alternativeChoiceDetails: [AlternativeChoiceDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/))<br>Called when a user has selected to make a purchase using alternative billing. |
---
title: BillingConfig
---

## BillingConfig

data class BillingConfig(val countryCode: String)

BillingConfig stores configuration used to perform billing operations.

Note: This data can change and should not be cached.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for BillingConfig](https://developer.android.com/reference/com/android/billingclient/api/BillingConfig).

### Constructors

| Name | Summary |
|---|---|
| BillingConfig | constructor(countryCode: String) |

### Properties

| Name | Summary |
|---|---|
| countryCode | val countryCode: String<br>The customer's country code. |
---
title: ProductDetailsResponseListener
---

## ProductDetailsResponseListener

interface ProductDetailsResponseListener

Listener to a result of product details query. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for ProductDetailsResponseListener](https://developer.android.com/reference/com/android/billingclient/api/ProductDetailsResponseListener).

### Functions

| Name | Summary |
|---|---|
| onProductDetailsResponse | abstract fun onProductDetailsResponse(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/), products: List&lt;[ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/)&gt;)<br>Called to notify that query product details operation has finished. |
---
title: Purchase
---

## Purchase

data class Purchase(val purchaseTime: Long, val purchaseToken: String, val products: List&lt;String&gt;, val packageName: String, val developerPayload: String? = &quot;&quot;, val orderId: String? = &quot;&quot;, val originalJson: String? = &quot;&quot;, val quantity: Int = 1, val signature: String = &quot;&quot;)

Represents an in-app billing purchase.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for Purchase](https://developer.android.com/reference/com/android/billingclient/api/Purchase).

### Constructors

| Name | Summary |
|---|---|
| Purchase | constructor(jsonPurchaseInfo: String, signature: String)constructor(purchaseTime: Long, purchaseToken: String, products: List&lt;String&gt;, packageName: String, developerPayload: String? = &quot;&quot;, orderId: String? = &quot;&quot;, originalJson: String? = &quot;&quot;, quantity: Int = 1, signature: String = &quot;&quot;) |

### Types

| Name | Summary |
|---|---|
| [PendingPurchaseUpdate](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase/pending-purchase-update/) | data class [PendingPurchaseUpdate](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase/pending-purchase-update/)(val products: List&lt;String&gt;, val purchaseToken: String)<br>Represents a pending change/update to the existing purchase. |
| [PurchaseState](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase/purchase-state/) | annotation class [PurchaseState](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase/purchase-state/)<br>Possible purchase states. |

### Properties

| Name | Summary |
|---|---|
| developerPayload | val developerPayload: String?<br>Returns the payload specified when the purchase was acknowledged or consumed. |
| orderId | val orderId: String?<br>Returns a unique order identifier for the transaction. |
| originalJson | val originalJson: String?<br>Returns a String in JSON format that contains details about the purchase order. |
| packageName | val packageName: String<br>Returns the application package from which the purchase originated. |
| products | val products: List&lt;String&gt;<br>Returns the product Ids. |
| purchaseTime | val purchaseTime: Long<br>Returns the time the product was purchased, in milliseconds since the epoch (Jan 1, 1970). |
| purchaseToken | val purchaseToken: String<br>Returns a token that uniquely identifies a purchase for a given item and user pair. |
| quantity | val quantity: Int = 1<br>Returns the quantity of the purchased product. |
| signature | val signature: String |

### Functions

| Name | Summary |
|---|---|
| getAccountIdentifiers | fun getAccountIdentifiers(): [AccountIdentifiers](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/account-identifiers/)<br>Returns account identifiers that were provided when the purchase was made. |
| getPendingPurchaseUpdate | fun getPendingPurchaseUpdate(): [Purchase.PendingPurchaseUpdate](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase/pending-purchase-update/)<br>Returns the PendingPurchaseUpdate for an uncommitted transaction. |
| getPurchaseState | fun getPurchaseState(): Int<br>Returns one of [PurchaseState](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/purchase/purchase-state/) indicating the state of the purchase. |
| getSkus | fun ~~getSkus~~(): List&lt;String&gt; |
| isAcknowledged | fun isAcknowledged(): Boolean<br>Indicates whether the purchase has been acknowledged. |
| isAutoRenewing | fun isAutoRenewing(): Boolean<br>Indicates whether the subscription renews automatically. |
---
title: AcknowledgePurchaseParams
---

## AcknowledgePurchaseParams

data class AcknowledgePurchaseParams(val purchaseToken: String)

Parameters to acknowledge a purchase. See BillingClient.acknowledgePurchase.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for AcknowledgePurchaseParams](https://developer.android.com/reference/com/android/billingclient/api/AcknowledgePurchaseParams).

### Constructors

| Name | Summary |
|---|---|
| AcknowledgePurchaseParams | constructor(purchaseToken: String) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/builder/) |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| purchaseToken | val purchaseToken: String<br>The token that identifies the purchase to be acknowledged. |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [AcknowledgePurchaseParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) |
---
title: PriceChangeFlowParams
---

## PriceChangeFlowParams

data class ~~PriceChangeFlowParams~~(val skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/))

#### Deprecated

This class has been marked as deprecated and removed from Play Billing Library since version 6.0.0.

---

Parameters to launch a price change confirmation flow.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for PriceChangeFlowParams](https://developer.android.com/reference/com/android/billingclient/api/PriceChangeFlowParams).

### Constructors

| Name | Summary |
|---|---|
| PriceChangeFlowParams | constructor(skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/)) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/builder/) | class [~~Builder~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/builder/)<br>Helps construct PriceChangeFlowParams that are used to launch a price change confirmation flow. |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| skuDetails | val skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/) |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [PriceChangeFlowParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) |
---
title: PendingPurchasesParams
---

## PendingPurchasesParams

class PendingPurchasesParams

Parameters to enable pending purchases.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for PendingPurchasesParams](https://developer.android.com/reference/com/android/billingclient/api/PendingPurchasesParams).

### Constructors

| Name | Summary |
|---|---|
| PendingPurchasesParams | constructor() |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/builder/) |
| Companion | object Companion |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [PendingPurchasesParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) |
---
title: BillingClient
---

## BillingClient

abstract class BillingClient

Main interface for communication between the library and user application code.

It provides convenience methods for in-app billing. You can create one instance of this class for your application and use it to process in-app billing operations. It provides synchronous (blocking) and asynchronous (non-blocking) methods for many common in-app billing operations.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for BillingClient](https://developer.android.com/reference/com/android/billingclient/api/BillingClient).

### Constructors

| Name | Summary |
|---|---|
| BillingClient | constructor() |

### Types

| Name | Summary |
|---|---|
| [AgeCategory](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/age-category/) | annotation class [AgeCategory](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/age-category/)<br>Age Category of the user. |
| [BillingResponseCode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/billing-response-code/) | annotation class [BillingResponseCode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/billing-response-code/)<br>Possible response codes. |
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/builder/)<br>Builder to configure and create a BillingClient instance. |
| Companion | object Companion |
| [ConnectionState](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/connection-state/) | annotation class [ConnectionState](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/connection-state/)<br>Connection state of billing client. |
| [FeatureType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/feature-type/) | annotation class [FeatureType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/feature-type/)<br>Features/capabilities supported by isFeatureSupported. |
| [ProductType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/product-type/) | annotation class [ProductType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/product-type/)<br>Supported Product types. |
| [SkuType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/sku-type/) | annotation class [~~SkuType~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/sku-type/)<br>Supported SKU types. |

### Functions

| Name | Summary |
|---|---|
| acknowledgePurchase | abstract fun acknowledgePurchase(params: [AcknowledgePurchaseParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/), listener: &lt;Error class: unknown class&gt;)<br>Acknowledges in-app purchases. |
| consumeAsync | abstract fun consumeAsync(params: [ConsumeParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/consume-params/), listener: &lt;Error class: unknown class&gt;)<br>Consumes a given in-app product. Consuming can only be done on an item that's owned, and as a result of consumption, the user will no longer own it. |
| createAlternativeBillingOnlyReportingDetailsAsync | abstract fun createAlternativeBillingOnlyReportingDetailsAsync(listener: &lt;Error class: unknown class&gt;)<br>Google Play Billing Library allows developers to create alternative billing only purchase details that can be used to report a transaction made via alternative billing without user choice to use Google Play billing. |
| createExternalOfferReportingDetailsAsync | abstract fun createExternalOfferReportingDetailsAsync(listener: &lt;Error class: unknown class&gt;)<br>Creates purchase details that can be used to report a transaction made via external offer. |
| endConnection | abstract fun endConnection()<br>Closes the connection and releases all held resources such as service connections. |
| getBillingConfigAsync | abstract fun getBillingConfigAsync(params: [GetBillingConfigParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/), listener: &lt;Error class: unknown class&gt;)<br>Gets the billing config, which stores configuration used to perform billing operations. |
| getConnectionState | abstract fun getConnectionState(): Int<br>Get the current billing client connection state. |
| isAlternativeBillingOnlyAvailableAsync | abstract fun isAlternativeBillingOnlyAvailableAsync(listener: &lt;Error class: unknown class&gt;)<br>In the Google Play Billing Library, this checks the availability of offering alternative billing without user choice to use Google Play billing. |
| isExternalOfferAvailableAsync | abstract fun isExternalOfferAvailableAsync(listener: &lt;Error class: unknown class&gt;)<br>Checks the availability of providing external offer. |
| isFeatureSupported | abstract fun isFeatureSupported(feature: String): [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/)<br>Checks if the specified feature or capability is supported. |
| isReady | abstract fun isReady(): Boolean<br>Checks if the client is currently connected to the service, so that requests to other methods will succeed. |
| launchBillingFlow | abstract fun launchBillingFlow(activity: &lt;Error class: unknown class&gt;, params: [BillingFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/)): [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/)<br>Initiates the billing flow for an in-app purchase or subscription. |
| launchPriceChangeConfirmationFlow | abstract fun ~~launchPriceChangeConfirmationFlow~~(activity: &lt;Error class: unknown class&gt;, params: [PriceChangeFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/), listener: &lt;Error class: unknown class&gt;)<br>Launch a price change confirmation flow. |
| queryAgeCategoryAsync | abstract fun queryAgeCategoryAsync(listener: &lt;Error class: unknown class&gt;)<br>Returns the AgeCategory of the user. |
| queryProductDetailsAsync | abstract fun queryProductDetailsAsync(params: [QueryProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/), listener: &lt;Error class: unknown class&gt;)<br>Performs a network query the details of products available for sale in your app. |
| queryPurchaseHistoryAsync | abstract fun ~~queryPurchaseHistoryAsync~~(queryPurchaseHistoryParams: [QueryPurchaseHistoryParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/), listener: &lt;Error class: unknown class&gt;)<br>abstract fun ~~queryPurchaseHistoryAsync~~(skuType: String, listener: &lt;Error class: unknown class&gt;)<br>Returns purchases details for items bought within your app. Only the most recent purchase made by the user for each SKU is returned. |
| queryPurchasesAsync | abstract fun queryPurchasesAsync(queryPurchasesParams: [QueryPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchases-params/), listener: &lt;Error class: unknown class&gt;)<br>abstract fun ~~queryPurchasesAsync~~(skuType: String, listener: &lt;Error class: unknown class&gt;)<br>Returns purchases details for currently owned items bought within your app. |
| querySkuDetailsAsync | abstract fun ~~querySkuDetailsAsync~~(params: [SkuDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details-params/), listener: &lt;Error class: unknown class&gt;)<br>Performs a network query to get SKU details and return the result asynchronously. |
| showAlternativeBillingOnlyInformationDialog | abstract fun showAlternativeBillingOnlyInformationDialog(activity: &lt;Error class: unknown class&gt;, listener: &lt;Error class: unknown class&gt;): [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/)<br>Shows the alternative billing only information dialog on top of the calling app. |
| showExternalOfferInformationDialog | abstract fun showExternalOfferInformationDialog(activity: &lt;Error class: unknown class&gt;, listener: &lt;Error class: unknown class&gt;): [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/)<br>Shows the external offer information dialog on top of the calling app. |
| showInAppMessages | abstract fun showInAppMessages(activity: &lt;Error class: unknown class&gt;, params: [InAppMessageParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-params/), listener: &lt;Error class: unknown class&gt;): [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/)<br>Overlays billing related messages on top of the calling app. |
| startConnection | abstract fun startConnection(listener: [BillingClientStateListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client-state-listener/))<br>Starts up BillingClient setup process asynchronously. You will be notified through the [BillingClientStateListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client-state-listener/) listener when the setup process is complete. |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| connectionState | var connectionState: Int |

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(context: &lt;Error class: unknown class&gt;): [BillingClient.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) |
---
title: PriceChangeConfirmationListener
---

## PriceChangeConfirmationListener

interface ~~PriceChangeConfirmationListener~~

#### Deprecated

---

Listener to a result of the price change confirmation flow. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for PriceChangeConfirmationListener](https://developer.android.com/reference/com/android/billingclient/api/PriceChangeConfirmationListener).

##### Deprecated

This class has been marked as deprecated and removed from Play Billing Library since version 6.0.0. To learn more about alternatives, see https://developer.android.com/google/play/billing/subscriptions#price-change.

### Functions

| Name | Summary |
|---|---|
| onPriceChangeConfirmationResult | abstract fun onPriceChangeConfirmationResult(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called to notify when a price change confirmation flow has finished. |
---
title: InAppMessageResult
---

## InAppMessageResult

data class InAppMessageResult(val purchaseToken: String, val responseCode: Int)

Results related to in-app messaging.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for InAppMessageResult](https://developer.android.com/reference/com/android/billingclient/api/InAppMessageResult).

### Constructors

| Name | Summary |
|---|---|
| InAppMessageResult | constructor(purchaseToken: String, responseCode: Int) |

### Types

| Name | Summary |
|---|---|
| [InAppMessageResponseCode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-result/in-app-message-response-code/) | annotation class [InAppMessageResponseCode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-result/in-app-message-response-code/)<br>Possible response codes. |

### Properties

| Name | Summary |
|---|---|
| purchaseToken | val purchaseToken: String<br>The token that identifies the purchase to be acknowledged, if any. |
| responseCode | val responseCode: Int<br>The response code for the in-app messaging API call. |
---
title: UserChoiceDetails
last_updated: 2025-03-19
---

## UserChoiceDetails

data class UserChoiceDetails(val externalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val originalExternalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[UserChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/)&gt;)

Details related to a user's choice of alternative billing.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for UserChoiceDetails](https://developer.android.com/reference/com/android/billingclient/api/UserChoiceDetails).

### Constructors

| Name | Summary |
|---|---|
| UserChoiceDetails | constructor(externalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), originalExternalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[UserChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/)&gt;) |

### Types

| Name | Summary |
|---|---|
| [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/) | data class [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/)(val id: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Properties

| Name | Summary |
|---|---|
| externalTransactionId | val externalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>A token that represents the user's prospective purchase via user choice alternative billing. |
| originalExternalTransactionId | val originalExternalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The external transaction Id of the originating subscription, if the purchase is a subscription upgrade/downgrade. |
| products | val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[UserChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/)&gt;<br>A list of [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/user-choice-details/product/) to be purchased in the user choice alternative billing flow. |
---
title: Builder
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [SkuDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details-params/) |
| setSkusList | fun setSkusList(skusList: List&lt;String&gt;): SkuDetailsParams.Builder |
| setType | fun setType(type: String): SkuDetailsParams.Builder |
---
title: SkuDetailsResponseListener
last_updated: 2025-03-19
---

## SkuDetailsResponseListener

interface ~~SkuDetailsResponseListener~~

#### Deprecated

---

Listener to a result of SKU details query. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for SkuDetailsResponseListener](https://developer.android.com/reference/com/android/billingclient/api/SkuDetailsResponseListener).

##### Deprecated

Use queryProductDetailsAsync instead.

### Functions

| Name | Summary |
|---|---|
| onSkuDetailsResponse | abstract fun onSkuDetailsResponse(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/), skuDetails: [List](https://docs.oracle.com/javase/8/docs/api/java/util/List.html)&lt;[SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/)&gt;)<br>Called to notify that a fetch SKU details operation has finished. |
---
title: Builder
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [QueryPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchases-params/)<br>Returns an instance of [QueryPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchases-params/). |
| setProductType | fun setProductType(productType: String): QueryPurchasesParams.Builder<br>Set the [BillingClient.ProductType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/product-type/) to query purchases. |
---
title: AgeCategoryResponseListener
---

## AgeCategoryResponseListener

interface AgeCategoryResponseListener

Listener to Age Category Response.

### Functions

| Name | Summary |
|---|---|
| onQueryAgeCategoryResponse | abstract fun onQueryAgeCategoryResponse(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/), ageCategory: Integer)<br>Called to notify that the query age category operation has finished. |
---
title: SkuDetails
last_updated: 2025-03-19
---

## SkuDetails

data class ~~SkuDetails~~(val price: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val priceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), val priceCurrencyCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val sku: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val subscriptionPeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val title: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val description: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val originalPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val originalPriceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html) = 0, val originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val introductoryPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val introductoryPriceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html) = 0, val introductoryPriceCycles: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 0, val introductoryPricePeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val iconUrl: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val freeTrialPeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;)

#### Deprecated

This class is deprecated. Use [BillingClient.queryProductDetailsAsync] instead.

---

Represents an in-app product's or subscription's listing details.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for SkuDetails](https://developer.android.com/reference/com/android/billingclient/api/SkuDetails).

### Constructors

| Name | Summary |
|---|---|
| SkuDetails | constructor(ovrProduct: Product)constructor(originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))constructor(price: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), priceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), priceCurrencyCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), sku: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), subscriptionPeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), title: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), description: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), originalPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, originalPriceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html) = 0, originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, introductoryPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, introductoryPriceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html) = 0, introductoryPriceCycles: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 0, introductoryPricePeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, iconUrl: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, freeTrialPeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;) |

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| description | val description: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Returns the description of the product. |
| freeTrialPeriod | val freeTrialPeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Trial period configured in the Developer Dashboard, specified in ISO 8601 format. For example, P7D equates to seven days. To learn more about free trial eligibility, see In-app Subscriptions. |
| iconUrl | val iconUrl: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Returns the icon of the product if present. |
| introductoryPrice | val introductoryPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Formatted introductory price of a subscription, including its currency sign, such as €3.99. For tax exclusive countries, the price doesn't include tax. |
| introductoryPriceAmountMicros | val introductoryPriceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html) = 0<br>Introductory price in micro-units. The currency is the same as price_currency_code. |
| introductoryPriceCycles | val introductoryPriceCycles: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 0<br>The number of subscription billing periods for which the user will be given the introductory price, such as 3. |
| introductoryPricePeriod | val introductoryPricePeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The billing period of the introductory price, specified in ISO 8601 format. |
| originalJson | val originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Returns a String in JSON format that contains SKU details. |
| originalPrice | val originalPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Returns formatted original price of the item, including its currency sign. |
| originalPriceAmountMicros | val originalPriceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html) = 0<br>Returns the original price in micro-units, where 1,000,000 micro-units equal one unit of the currency. |
| price | val price: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Returns formatted price of the item, including its currency sign. |
| priceAmountMicros | val priceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html)<br>Returns price in micro-units, where 1,000,000 micro-units equal one unit of the currency. |
| priceCurrencyCode | val priceCurrencyCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Returns ISO 4217 currency code for price and original price. |
| sku | val sku: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Returns the product Id. |
| subscriptionPeriod | val subscriptionPeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Subscription period, specified in ISO 8601 format. For example, P1W equates to one week, P1M equates to one month, P3M equates to three months, P6M equates to six months, and P1Y equates to one year. |
| title | val title: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Returns the title of the product being sold. |
| type | val type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Returns the {@link BillingClient.SkuType} of the SKU. |

## Companion

object Companion
---
title: SkuDetailsParams
last_updated: 2025-03-19
---

## SkuDetailsParams

data class ~~SkuDetailsParams~~(val skuType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val skusList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;)

#### Deprecated

Use [BillingClient.queryProductDetailsAsync] instead

---

Parameters to initiate a query for SKU details. See [BillingClient.querySkuDetailsAsync](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/).

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for SkuDetailsParams](https://developer.android.com/reference/com/android/billingclient/api/SkuDetailsParams).

### Constructors

| Name | Summary |
|---|---|
| SkuDetailsParams | constructor(skuType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), skusList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details-params/builder/) |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| skusList | val skusList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;<br>The list of SKUs to query. |
| skuType | val skuType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The SkuType of the SKUs to query. |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [SkuDetailsParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details-params/builder/) |
---
title: ProductDetails
---

## ProductDetails

data class ProductDetails(val productId: String, val title: String = &quot;&quot;, val name: String = &quot;&quot;, val description: String = &quot;&quot;, val productType: String, val oneTimePurchaseOfferDetails: [ProductDetails.OneTimePurchaseOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/one-time-purchase-offer-details/)?, var subscriptionOfferDetails: List&lt;[ProductDetails.SubscriptionOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/subscription-offer-details/)&gt;?)

Represents the details of a one time or subscription product.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for ProductDetails](https://developer.android.com/reference/com/android/billingclient/api/ProductDetails).

### Constructors

| Name | Summary |
|---|---|
| ProductDetails | constructor(ovrProduct: &lt;Error class: unknown class&gt;)constructor(productId: String, title: String = &quot;&quot;, name: String = &quot;&quot;, description: String = &quot;&quot;, productType: String, oneTimePurchaseOfferDetails: [ProductDetails.OneTimePurchaseOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/one-time-purchase-offer-details/)?, subscriptionOfferDetails: List&lt;[ProductDetails.SubscriptionOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/subscription-offer-details/)&gt;?) |

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |
| [InstallmentPlanDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/installment-plan-details/) | data class [InstallmentPlanDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/installment-plan-details/)(val installmentPlanCommitmentPaymentsCount: Int, val subsequentInstallmentPlanCommitmentPaymentsCount: Int)<br>Represents additional details of an installment subscription plan. |
| [OneTimePurchaseOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/one-time-purchase-offer-details/) | data class [OneTimePurchaseOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/one-time-purchase-offer-details/)(val formattedPrice: String, val priceAmountMicros: Long, val priceCurrencyCode: String)<br>Represents the offer details to buy an one-time purchase product. |
| [PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/) | data class [PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/)(val billingCycleCount: Int, val billingPeriod: String, val formattedPrice: String, val priceAmountMicros: Long, val priceCurrencyCode: String, val recurrenceMode: Int)<br>Represents a pricing phase, describing how a user pays at a point in time. |
| [PricingPhases](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phases/) | data class [PricingPhases](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phases/)(val pricingPhaseList: List&lt;[ProductDetails.PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/)&gt;)<br>Pricing phases for purchasing an item through a offer. Pricing phases contains time ordered list of [ProductDetails.PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/). |
| [RecurrenceMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/recurrence-mode/) | annotation class [RecurrenceMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/recurrence-mode/)<br>Recurrence mode of the pricing phase. |
| [SubscriptionOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/subscription-offer-details/) | data class [SubscriptionOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/subscription-offer-details/)(val basePlanId: String, val installmentPlanDetails: [ProductDetails.InstallmentPlanDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/installment-plan-details/), val offerId: String?, val offerTags: List&lt;String&gt;, val offerToken: String, val pricingPhases: [ProductDetails.PricingPhases](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phases/))<br>Represents the available purchase plans to buy a subscription product. |

### Properties

| Name | Summary |
|---|---|
| description | val description: String<br>The description of the product. |
| name | val name: String<br>The name of the product being sold. |
| oneTimePurchaseOfferDetails | val oneTimePurchaseOfferDetails: [ProductDetails.OneTimePurchaseOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/one-time-purchase-offer-details/)?<br>The offer details of an one-time purchase product. |
| productId | val productId: String<br>The product's Id. |
| productType | val productType: String<br>The @BillingClient.ProductType of the product |
| subscriptionOfferDetails | var subscriptionOfferDetails: List&lt;[ProductDetails.SubscriptionOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/subscription-offer-details/)&gt;?<br>The available purchase plans to buy a subscription product. |
| title | val title: String<br>The title of the product being sold. |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| SUBS_VIRTUAL_SKU_PREFIX | const val SUBS_VIRTUAL_SKU_PREFIX: String |
---
title: QueryPurchasesParams
last_updated: 2025-03-19
---

## QueryPurchasesParams

data class QueryPurchasesParams(val productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

Parameters to initiate a query for purchases.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for QueryPurchasesParams](https://developer.android.com/reference/com/android/billingclient/api/QueryPurchasesParams).

### Constructors

| Name | Summary |
|---|---|
| QueryPurchasesParams | constructor(productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchases-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchases-params/builder/) |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| productType | val productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [QueryPurchasesParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchases-params/builder/)<br>Constructs a new [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchases-params/builder/) instance. |
---
title: PurchasesResponseListener
last_updated: 2025-03-19
---

## PurchasesResponseListener

interface PurchasesResponseListener

Listener to a result of purchases query. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for PurchasesResponseListener](https://developer.android.com/reference/com/android/billingclient/api/PurchasesResponseListener).

### Functions

| Name | Summary |
|---|---|
| onQueryPurchasesResponse | abstract fun onQueryPurchasesResponse(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/), purchases: [List](https://docs.oracle.com/javase/8/docs/api/java/util/List.html)&lt;[Purchase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase/)&gt;)<br>Called to notify that the query purchases operation has finished. |
---
title: PurchasesUpdatedListener
last_updated: 2025-03-19
---

## PurchasesUpdatedListener

interface PurchasesUpdatedListener

Listener interface for purchase updates which happen when, for example, the user buys something within the app or by initiating a purchase from the Store. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for PurchasesUpdatedListener](https://developer.android.com/reference/com/android/billingclient/api/PurchasesUpdatedListener).

### Functions

| Name | Summary |
|---|---|
| onPurchasesUpdated | abstract fun onPurchasesUpdated(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/), purchases: [List](https://docs.oracle.com/javase/8/docs/api/java/util/List.html)&lt;[Purchase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase/)&gt;) |
---
title: PurchaseHistoryResponseListener
last_updated: 2025-03-19
---

## PurchaseHistoryResponseListener

interface PurchaseHistoryResponseListener

Listener to a result of purchase history query. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for PurchaseHistoryResponseListener](https://developer.android.com/reference/com/android/billingclient/api/PurchaseHistoryResponseListener).

### Functions

| Name | Summary |
|---|---|
| onPurchaseHistoryResponse | abstract fun onPurchaseHistoryResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/), purchaseHistoryRecordList: [List](https://docs.oracle.com/javase/8/docs/api/java/util/List.html)&lt;[PurchaseHistoryRecord](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase-history-record/)&gt;)<br>Called to notify that the query purchase history operation has finished. |
---
title: InAppMessageParams
---

## InAppMessageParams

class InAppMessageParams(inAppMessageCategoriesSet: Set&lt;Int&gt;)

Parameters for in-app messaging. See BillingClient.showInAppMessages.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for InAppMessageParams](https://developer.android.com/reference/com/android/billingclient/api/InAppMessageParams).

### Constructors

| Name | Summary |
|---|---|
| InAppMessageParams | constructor(inAppMessageCategoriesSet: Set&lt;Int&gt;) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-params/builder/)<br>Helps construct InAppMessageParams. |
| Companion | object Companion |
| [InAppMessageCategoryId](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-params/in-app-message-category-id/) | annotation class [InAppMessageCategoryId](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-params/in-app-message-category-id/)<br>A high-level category of the in-app message. |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [InAppMessageParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) |
---
title: UserChoiceBillingListener
---

## UserChoiceBillingListener

interface UserChoiceBillingListener

Listener interface for the developer-managed alternative billing flow, when it is chosen by the user when initiating a purchase. 

Alternative Billing for IAP is not supported by Meta. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for UserChoiceBillingListener](https://developer.android.com/reference/com/android/billingclient/api/UserChoiceBillingListener).

### Functions

| Name | Summary |
|---|---|
| userSelectedAlternativeBilling | abstract fun userSelectedAlternativeBilling(userChoiceDetails: [UserChoiceDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/user-choice-details/))<br>Called when a user has selected to make a purchase using user choice billing. |
---
title: PurchaseHistoryRecord
last_updated: 2025-03-19
---

## PurchaseHistoryRecord

data class PurchaseHistoryRecord(val purchaseTime: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;, val developerPayload: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, val originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, val quantity: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1, val signature: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;)

Represents an in-app billing purchase history record.

This class includes a subset of fields in [Purchase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase/).

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for PurchaseHistoryRecord](https://developer.android.com/reference/com/android/billingclient/api/PurchaseHistoryRecord).

### Constructors

| Name | Summary |
|---|---|
| PurchaseHistoryRecord | constructor(jsonPurchaseInfo: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), signature: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))constructor(purchaseTime: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;, developerPayload: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, quantity: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1, signature: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;) |

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| developerPayload | val developerPayload: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)?<br>Returns the payload specified when the purchase was acknowledged or consumed. |
| originalJson | val originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)?<br>Returns a String in JSON format that contains details about the purchase order. |
| products | val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;<br>Returns the product Ids. |
| purchaseTime | val purchaseTime: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html)<br>Returns the time the product was purchased, in milliseconds since the epoch (Jan 1, 1970). |
| purchaseToken | val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Returns a token that uniquely identifies a purchase for a given item and user pair. |
| quantity | val quantity: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1<br>Returns the quantity of the purchased product. |
| signature | val signature: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>String containing the signature of the purchase data that was signed with the private key of the developer. |

### Functions

| Name | Summary |
|---|---|
| getSkus | fun ~~getSkus~~(): &lt;Error class: unknown class&gt;&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;<br>Returns the product Ids. |

## Companion

object Companion
---
title: ExternalOfferReportingDetailsListener
---

## ExternalOfferReportingDetailsListener

interface ExternalOfferReportingDetailsListener

Listener for the result of the createExternalOfferReportingDetailsAsync API. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for ExternalOfferReportingDetailsListener](https://developer.android.com/reference/com/android/billingclient/api/ExternalOfferReportingDetailsListener).

### Functions

| Name | Summary |
|---|---|
| onExternalOfferReportingDetailsResponse | abstract fun onExternalOfferReportingDetailsResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/), externalOfferReportingDetails: [ExternalOfferReportingDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/external-offer-reporting-details/))<br>Called to receive the results from createExternalOfferReportingDetailsAsync when it is finished. |
---
title: PriceChangeFlowParams
last_updated: 2025-03-19
---

## PriceChangeFlowParams

data class ~~PriceChangeFlowParams~~(val skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/))

#### Deprecated

This class has been marked as deprecated and removed from Play Billing Library since version 6.0.0.

---

Parameters to launch a price change confirmation flow.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for PriceChangeFlowParams](https://developer.android.com/reference/com/android/billingclient/api/PriceChangeFlowParams).

### Constructors

| Name | Summary |
|---|---|
| PriceChangeFlowParams | constructor(skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/)) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/builder/) | class [~~Builder~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/builder/)<br>Helps construct PriceChangeFlowParams that are used to launch a price change confirmation flow. |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| skuDetails | val skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/) |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [PriceChangeFlowParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/builder/) |
---
title: ConsumeResponseListener
---

## ConsumeResponseListener

interface ConsumeResponseListener

Callback that notifies when a consumption operation finishes. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for ConsumeResponseListener](https://developer.android.com/reference/com/android/billingclient/api/ConsumeResponseListener).

### Functions

| Name | Summary |
|---|---|
| onConsumeResponse | abstract fun onConsumeResponse(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/), purchaseToken: String)<br>Called to notify that a consume operation has finished. |
---
title: Purchase
last_updated: 2025-03-19
---

## Purchase

data class Purchase(val purchaseTime: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;, val packageName: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val developerPayload: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, val orderId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, val originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, val quantity: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1, val signature: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;)

Represents an in-app billing purchase.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for Purchase](https://developer.android.com/reference/com/android/billingclient/api/Purchase).

### Constructors

| Name | Summary |
|---|---|
| Purchase | constructor(jsonPurchaseInfo: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), signature: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))constructor(purchaseTime: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;, packageName: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), developerPayload: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, orderId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = &quot;&quot;, quantity: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1, signature: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;) |

### Types

| Name | Summary |
|---|---|
| [PendingPurchaseUpdate](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase/pending-purchase-update/) | data class [PendingPurchaseUpdate](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase/pending-purchase-update/)(val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;, val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>Represents a pending change/update to the existing purchase. |
| [PurchaseState](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase/purchase-state/) | annotation class [PurchaseState](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase/purchase-state/)<br>Possible purchase states. |

### Properties

| Name | Summary |
|---|---|
| developerPayload | val developerPayload: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)?<br>Returns the payload specified when the purchase was acknowledged or consumed. |
| orderId | val orderId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)?<br>Returns a unique order identifier for the transaction. |
| originalJson | val originalJson: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)?<br>Returns a String in JSON format that contains details about the purchase order. |
| packageName | val packageName: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Returns the application package from which the purchase originated. |
| products | val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;<br>Returns the product Ids. |
| purchaseTime | val purchaseTime: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html)<br>Returns the time the product was purchased, in milliseconds since the epoch (Jan 1, 1970). |
| purchaseToken | val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Returns a token that uniquely identifies a purchase for a given item and user pair. |
| quantity | val quantity: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1<br>Returns the quantity of the purchased product. |
| signature | val signature: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) |

### Functions

| Name | Summary |
|---|---|
| getAccountIdentifiers | fun getAccountIdentifiers(): [AccountIdentifiers](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/account-identifiers/)<br>Returns account identifiers that were provided when the purchase was made. |
| getPendingPurchaseUpdate | fun getPendingPurchaseUpdate(): [Purchase.PendingPurchaseUpdate](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase/pending-purchase-update/)<br>Returns the PendingPurchaseUpdate for an uncommitted transaction. |
| getPurchaseState | fun getPurchaseState(): [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)<br>Returns one of [PurchaseState](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/purchase/purchase-state/) indicating the state of the purchase. |
| getSkus | fun ~~getSkus~~(): [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt; |
| isAcknowledged | fun isAcknowledged(): [Boolean](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/boolean/index.html)<br>Indicates whether the purchase has been acknowledged. |
| isAutoRenewing | fun isAutoRenewing(): [Boolean](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/boolean/index.html)<br>Indicates whether the subscription renews automatically. |
---
title: ExternalOfferAvailabilityListener
---

## ExternalOfferAvailabilityListener

interface ExternalOfferAvailabilityListener

Listener for the result of the isExternalOfferAvailableAsync API. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for ExternalOfferAvailabilityListener](https://developer.android.com/reference/com/android/billingclient/api/ExternalOfferAvailabilityListener).

### Functions

| Name | Summary |
|---|---|
| onExternalOfferAvailabilityResponse | abstract fun onExternalOfferAvailabilityResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called to receive the results from isExternalOfferAvailableAsync when it is finished. |
---
title: QueryProductDetailsParams
last_updated: 2025-03-19
---

## QueryProductDetailsParams

data class QueryProductDetailsParams(val productList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[QueryProductDetailsParams.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)&gt;)

Parameters to initiate a query for Product details [BillingClient.queryProductDetailsAsync](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/).

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for QueryProductDetailsParams](https://developer.android.com/reference/com/android/billingclient/api/QueryProductDetailsParams).

### Constructors

| Name | Summary |
|---|---|
| QueryProductDetailsParams | constructor(productList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[QueryProductDetailsParams.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)&gt;) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/builder/) |
| Companion | object Companion |
| [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/) | data class [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)(val productId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>A Product identifier used for querying product details. |

### Properties

| Name | Summary |
|---|---|
| productList | val productList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[QueryProductDetailsParams.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)&gt; |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [QueryProductDetailsParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/builder/)<br>Constructs a new [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/builder/) instance. |
---
title: ProductDetailsResponseListener
last_updated: 2025-03-19
---

## ProductDetailsResponseListener

interface ProductDetailsResponseListener

Listener to a result of product details query. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for ProductDetailsResponseListener](https://developer.android.com/reference/com/android/billingclient/api/ProductDetailsResponseListener).

### Functions

| Name | Summary |
|---|---|
| onProductDetailsResponse | abstract fun onProductDetailsResponse(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/), products: [List](https://docs.oracle.com/javase/8/docs/api/java/util/List.html)&lt;[ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/)&gt;)<br>Called to notify that query product details operation has finished. |
---
title: GetBillingConfigParams
---

## GetBillingConfigParams

class GetBillingConfigParams

Parameters for get billing config flow BillingClient.getBillingConfigAsync.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for GetBillingConfigParams](https://developer.android.com/reference/com/android/billingclient/api/GetBillingConfigParams).

### Constructors

| Name | Summary |
|---|---|
| GetBillingConfigParams | constructor() |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/builder/)<br>Helps construct GetBillingConfigParams. |
| Companion | object Companion |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [GetBillingConfigParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/)<br>Constructs a new [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) instance. |
---
title: PendingPurchasesParams
last_updated: 2025-03-19
---

## PendingPurchasesParams

class PendingPurchasesParams

Parameters to enable pending purchases.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for PendingPurchasesParams](https://developer.android.com/reference/com/android/billingclient/api/PendingPurchasesParams).

### Constructors

| Name | Summary |
|---|---|
| PendingPurchasesParams | constructor() |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/builder/) |
| Companion | object Companion |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [PendingPurchasesParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/builder/) |
---
title: ExternalOfferInformationDialogListener
---

## ExternalOfferInformationDialogListener

interface ExternalOfferInformationDialogListener

Listener for the result of the [BillingClient.showExternalOfferInformationDialog] API. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for ExternalOfferInformationDialogListener](https://developer.android.com/reference/com/android/billingclient/api/ExternalOfferInformationDialogListener).

### Functions

| Name | Summary |
|---|---|
| onExternalOfferInformationDialogResponse | abstract fun onExternalOfferInformationDialogResponse(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called to notify that the external offer information dialog flow is finished. |
---
title: PriceChangeConfirmationListener
---

## PriceChangeConfirmationListener

interface ~~PriceChangeConfirmationListener~~

#### Deprecated

---

Listener to a result of the price change confirmation flow. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for PriceChangeConfirmationListener](https://developer.android.com/reference/com/android/billingclient/api/PriceChangeConfirmationListener).

##### Deprecated

This class has been marked as deprecated and removed from Play Billing Library since version 6.0.0. To learn more about alternatives, see https://developer.android.com/google/play/billing/subscriptions#price-change.

### Functions

| Name | Summary |
|---|---|
| onPriceChangeConfirmationResult | abstract fun onPriceChangeConfirmationResult(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called to notify when a price change confirmation flow has finished. |
---
title: ConsumeParams
---

## ConsumeParams

data class ConsumeParams(val purchaseToken: String)

Parameters to consume a purchase. See BillingClient.consumeAsync.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for ConsumeParams](https://developer.android.com/reference/com/android/billingclient/api/ConsumeParams).

### Constructors

| Name | Summary |
|---|---|
| ConsumeParams | constructor(purchaseToken: String) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/consume-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/consume-params/builder/) |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| purchaseToken | val purchaseToken: String |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [ConsumeParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) |
---
title: AcknowledgePurchaseResponseListener
---

## AcknowledgePurchaseResponseListener

interface AcknowledgePurchaseResponseListener

Listener for the result of an acknowledge purchase request. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for AcknowledgePurchaseResponseListener](https://developer.android.com/reference/com/android/billingclient/api/AcknowledgePurchaseResponseListener).

### Functions

| Name | Summary |
|---|---|
| onAcknowledgePurchaseResponse | abstract fun onAcknowledgePurchaseResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called to notify that an acknowledge purchase operation has finished. |
---
title: ExternalOfferReportingDetails
last_updated: 2025-03-19
---

## ExternalOfferReportingDetails

data class ExternalOfferReportingDetails(val externalTransactionToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

The details used to report transactions made via external offer.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for ExternalOfferReportingDetails](https://developer.android.com/reference/com/android/billingclient/api/ExternalOfferReportingDetails).

### Constructors

| Name | Summary |
|---|---|
| ExternalOfferReportingDetails | constructor(externalTransactionToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Properties

| Name | Summary |
|---|---|
| externalTransactionToken | val externalTransactionToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>An external transaction token that can be used to report a transaction made via external offer. |
---
title: ExternalOfferReportingDetails
---

## ExternalOfferReportingDetails

data class ExternalOfferReportingDetails(val externalTransactionToken: String)

The details used to report transactions made via external offer.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for ExternalOfferReportingDetails](https://developer.android.com/reference/com/android/billingclient/api/ExternalOfferReportingDetails).

### Constructors

| Name | Summary |
|---|---|
| ExternalOfferReportingDetails | constructor(externalTransactionToken: String) |

### Properties

| Name | Summary |
|---|---|
| externalTransactionToken | val externalTransactionToken: String<br>An external transaction token that can be used to report a transaction made via external offer. |
---
title: BillingConfigResponseListener
---

## BillingConfigResponseListener

interface BillingConfigResponseListener

Listener for the result of the getBillingConfigAsync API. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for BillingConfigResponseListener](https://developer.android.com/reference/com/android/billingclient/api/BillingConfigResponseListener).

### Functions

| Name | Summary |
|---|---|
| onBillingConfigResponse | abstract fun onBillingConfigResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/), billingConfig: [BillingConfig](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-config/))<br>Called to notify when the get billing config flow has finished. |
---
title: ConsumeParams
last_updated: 2025-03-19
---

## ConsumeParams

data class ConsumeParams(val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

Parameters to consume a purchase. See [BillingClient.consumeAsync](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/).

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for ConsumeParams](https://developer.android.com/reference/com/android/billingclient/api/ConsumeParams).

### Constructors

| Name | Summary |
|---|---|
| ConsumeParams | constructor(purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/consume-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/consume-params/builder/) |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| purchaseToken | val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [ConsumeParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/consume-params/builder/) |
---
title: GetBillingConfigParams
last_updated: 2025-03-19
---

## GetBillingConfigParams

class GetBillingConfigParams

Parameters for get billing config flow [BillingClient.getBillingConfigAsync](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/).

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for GetBillingConfigParams](https://developer.android.com/reference/com/android/billingclient/api/GetBillingConfigParams).

### Constructors

| Name | Summary |
|---|---|
| GetBillingConfigParams | constructor() |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/builder/)<br>Helps construct GetBillingConfigParams. |
| Companion | object Companion |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [GetBillingConfigParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/builder/)<br>Constructs a new [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/builder/) instance. |
---
title: QueryPurchaseHistoryParams
last_updated: 2025-03-19
---

## QueryPurchaseHistoryParams

data class QueryPurchaseHistoryParams(val productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

Parameters to initiate a query for purchase history.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for QueryPurchaseHistoryParams](https://developer.android.com/reference/com/android/billingclient/api/QueryPurchaseHistoryParams).

### Constructors

| Name | Summary |
|---|---|
| QueryPurchaseHistoryParams | constructor(productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/builder/) |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| productType | val productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [QueryPurchaseHistoryParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/builder/)<br>Constructs a new [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/builder/) instance. |
---
title: ConsumeResponseListener
last_updated: 2025-03-19
---

## ConsumeResponseListener

interface ConsumeResponseListener

Callback that notifies when a consumption operation finishes. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for ConsumeResponseListener](https://developer.android.com/reference/com/android/billingclient/api/ConsumeResponseListener).

### Functions

| Name | Summary |
|---|---|
| onConsumeResponse | abstract fun onConsumeResponse(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/), purchaseToken: [String](https://docs.oracle.com/javase/8/docs/api/java/lang/String.html))<br>Called to notify that a consume operation has finished. |
---
title: ExternalOfferAvailabilityListener
---

## ExternalOfferAvailabilityListener

interface ExternalOfferAvailabilityListener

Listener for the result of the isExternalOfferAvailableAsync API. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for ExternalOfferAvailabilityListener](https://developer.android.com/reference/com/android/billingclient/api/ExternalOfferAvailabilityListener).

### Functions

| Name | Summary |
|---|---|
| onExternalOfferAvailabilityResponse | abstract fun onExternalOfferAvailabilityResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called to receive the results from isExternalOfferAvailableAsync when it is finished. |
---
title: ProductDetails
last_updated: 2025-03-19
---

## ProductDetails

data class ProductDetails(val productId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val title: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val name: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val description: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, val productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val oneTimePurchaseOfferDetails: [ProductDetails.OneTimePurchaseOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/one-time-purchase-offer-details/)?, var subscriptionOfferDetails: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[ProductDetails.SubscriptionOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/subscription-offer-details/)&gt;?)

Represents the details of a one time or subscription product.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for ProductDetails](https://developer.android.com/reference/com/android/billingclient/api/ProductDetails).

### Constructors

| Name | Summary |
|---|---|
| ProductDetails | constructor(ovrProduct: Product)constructor(productId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), title: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, name: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, description: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) = &quot;&quot;, productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), oneTimePurchaseOfferDetails: [ProductDetails.OneTimePurchaseOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/one-time-purchase-offer-details/)?, subscriptionOfferDetails: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[ProductDetails.SubscriptionOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/subscription-offer-details/)&gt;?) |

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |
| [InstallmentPlanDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/installment-plan-details/) | data class [InstallmentPlanDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/installment-plan-details/)(val installmentPlanCommitmentPaymentsCount: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html), val subsequentInstallmentPlanCommitmentPaymentsCount: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html))<br>Represents additional details of an installment subscription plan. |
| [OneTimePurchaseOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/one-time-purchase-offer-details/) | data class [OneTimePurchaseOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/one-time-purchase-offer-details/)(val formattedPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val priceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), val priceCurrencyCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>Represents the offer details to buy an one-time purchase product. |
| [PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/) | data class [PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/)(val billingCycleCount: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html), val billingPeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val formattedPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val priceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), val priceCurrencyCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val recurrenceMode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html))<br>Represents a pricing phase, describing how a user pays at a point in time. |
| [PricingPhases](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phases/) | data class [PricingPhases](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phases/)(val pricingPhaseList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[ProductDetails.PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/)&gt;)<br>Pricing phases for purchasing an item through a offer. Pricing phases contains time ordered list of [ProductDetails.PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/). |
| [RecurrenceMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/recurrence-mode/) | annotation class [RecurrenceMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/recurrence-mode/)<br>Recurrence mode of the pricing phase. |
| [SubscriptionOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/subscription-offer-details/) | data class [SubscriptionOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/subscription-offer-details/)(val basePlanId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val installmentPlanDetails: [ProductDetails.InstallmentPlanDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/installment-plan-details/), val offerId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)?, val offerTags: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;, val offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val pricingPhases: [ProductDetails.PricingPhases](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phases/))<br>Represents the available purchase plans to buy a subscription product. |

### Properties

| Name | Summary |
|---|---|
| description | val description: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The description of the product. |
| name | val name: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The name of the product being sold. |
| oneTimePurchaseOfferDetails | val oneTimePurchaseOfferDetails: [ProductDetails.OneTimePurchaseOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/one-time-purchase-offer-details/)?<br>The offer details of an one-time purchase product. |
| productId | val productId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The product's Id. |
| productType | val productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The @BillingClient.ProductType of the product |
| subscriptionOfferDetails | var subscriptionOfferDetails: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[ProductDetails.SubscriptionOfferDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/subscription-offer-details/)&gt;?<br>The available purchase plans to buy a subscription product. |
| title | val title: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The title of the product being sold. |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| SUBS_VIRTUAL_SKU_PREFIX | const val SUBS_VIRTUAL_SKU_PREFIX: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) |
---
title: InAppMessageResult
last_updated: 2025-03-19
---

## InAppMessageResult

data class InAppMessageResult(val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val responseCode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html))

Results related to in-app messaging.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for InAppMessageResult](https://developer.android.com/reference/com/android/billingclient/api/InAppMessageResult).

### Constructors

| Name | Summary |
|---|---|
| InAppMessageResult | constructor(purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), responseCode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)) |

### Types

| Name | Summary |
|---|---|
| [InAppMessageResponseCode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-result/in-app-message-response-code/) | annotation class [InAppMessageResponseCode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-result/in-app-message-response-code/)<br>Possible response codes. |

### Properties

| Name | Summary |
|---|---|
| purchaseToken | val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The token that identifies the purchase to be acknowledged, if any. |
| responseCode | val responseCode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)<br>The response code for the in-app messaging API call. |
---
title: BillingClientStateListener
---

## BillingClientStateListener

interface BillingClientStateListener

Callback for setup process. This listener's BillingClient.onBillingSetupFinished method is called when the setup process is complete.

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for BillingClientStateListener](https://developer.android.com/reference/com/android/billingclient/api/BillingClientStateListener).

### Functions

| Name | Summary |
|---|---|
| onBillingServiceDisconnected | abstract fun onBillingServiceDisconnected()<br>Called to notify that the connection to the billing service was lost. |
| onBillingSetupFinished | abstract fun onBillingSetupFinished(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called to notify that setup is complete. |
---
title: InAppMessageParams
last_updated: 2025-03-19
---

## InAppMessageParams

class InAppMessageParams(inAppMessageCategoriesSet: [Set](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/set/index.html)&lt;[Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)&gt;)

Parameters for in-app messaging. See [BillingClient.showInAppMessages](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/).

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for InAppMessageParams](https://developer.android.com/reference/com/android/billingclient/api/InAppMessageParams).

### Constructors

| Name | Summary |
|---|---|
| InAppMessageParams | constructor(inAppMessageCategoriesSet: [Set](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/set/index.html)&lt;[Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)&gt;) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-params/builder/)<br>Helps construct InAppMessageParams. |
| Companion | object Companion |
| [InAppMessageCategoryId](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-params/in-app-message-category-id/) | annotation class [InAppMessageCategoryId](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-params/in-app-message-category-id/)<br>A high-level category of the in-app message. |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [InAppMessageParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-params/builder/) |
---
title: InAppMessageResponseListener
---

## InAppMessageResponseListener

interface InAppMessageResponseListener

Listener for the result of the in-app messaging flow. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for InAppMessageResponseListener](https://developer.android.com/reference/com/android/billingclient/api/InAppMessageResponseListener).

### Functions

| Name | Summary |
|---|---|
| onInAppMessageResponse | abstract fun onInAppMessageResponse(inAppMessageResult: [InAppMessageResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-result/))<br>Called to notify when the in-app messaging flow has finished. |
---
title: BillingFlowParams
---

## BillingFlowParams

data class BillingFlowParams(val obfuscatedAccountId: String? = null, val obfuscatedProfileId: String? = null, val isOfferPersonalized: Boolean = false, val productDetailsParamsList: List&lt;[BillingFlowParams.ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/)&gt; = emptyList(), val subscriptionUpdateParams: [BillingFlowParams.SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/)? = null, val skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/)? = null)

Parameters to initiate a purchase flow. See BillingClient.launchBillingFlow.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for BillingFlowParams](https://developer.android.com/reference/com/android/billingclient/api/BillingFlowParams).

### Constructors

| Name | Summary |
|---|---|
| BillingFlowParams | constructor(obfuscatedAccountId: String? = null, obfuscatedProfileId: String? = null, isOfferPersonalized: Boolean = false, productDetailsParamsList: List&lt;[BillingFlowParams.ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/)&gt; = emptyList(), subscriptionUpdateParams: [BillingFlowParams.SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/)? = null, skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/)? = null) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/builder/)<br>Helps to construct BillingFlowParams that are used to initiate a purchase flow. |
| Companion | object Companion |
| [ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/) | data class [ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/)(val productDetails: [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/), val offerToken: String? = null)<br>Params that describe the product to be purchased and the offer to purchase with. |
| [ProrationMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/proration-mode/) | annotation class [~~ProrationMode~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/proration-mode/)<br>Replace SKU ProrationMode. |
| [SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/) | class [SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/)(oldPurchaseToken: String? = null, externalTransactionId: String? = null, subscriptionReplacementMode: Int? = null)<br>Params that describe a subscription update. |

### Properties

| Name | Summary |
|---|---|
| isOfferPersonalized | val isOfferPersonalized: Boolean = false |
| obfuscatedAccountId | val obfuscatedAccountId: String? = null |
| obfuscatedProfileId | val obfuscatedProfileId: String? = null |
| productDetailsParamsList | val productDetailsParamsList: List&lt;[BillingFlowParams.ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/)&gt; |
| skuDetails | val ~~skuDetails~~: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/)? = null |
| subscriptionUpdateParams | val subscriptionUpdateParams: [BillingFlowParams.SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/)? = null |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| EXTRA_PARAM_KEY_ACCOUNT_ID | const val EXTRA_PARAM_KEY_ACCOUNT_ID: String |

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [BillingFlowParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) |
---
title: BillingResult
---

## BillingResult

data class BillingResult(val responseCode: Int, val debugMessage: String)

Params containing the response code and the debug message from In-app Billing API response.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for BillingResult](https://developer.android.com/reference/com/android/billingclient/api/BillingResult).

### Constructors

| Name | Summary |
|---|---|
| BillingResult | constructor(responseCode: Int, debugMessage: String) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/builder/)<br>Helps to construct BillingResult that are used to return response from In-app Billing API. |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| debugMessage | val debugMessage: String<br>Debug message returned in In-app Billing API calls. |
| responseCode | val responseCode: Int<br>Response code returned in In-app Billing API calls. |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [BillingResult.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/builder/) |
---
title: AlternativeBillingOnlyReportingDetailsListener
---

## AlternativeBillingOnlyReportingDetailsListener

interface AlternativeBillingOnlyReportingDetailsListener

Listener for the result of the createAlternativeBillingOnlyReportingDetailsAsync API. 

Alternative Billing for IAP is not supported by Meta. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for AlternativeBillingOnlyReportingDetailsListener](https://developer.android.com/reference/com/android/billingclient/api/AlternativeBillingOnlyReportingDetailsListener).

### Functions

| Name | Summary |
|---|---|
| onAlternativeBillingOnlyTokenResponse | abstract fun onAlternativeBillingOnlyTokenResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/), alternativeBillingOnlyReportingDetails: [AlternativeBillingOnlyReportingDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-billing-only-reporting-details/))<br>Called to receive the results from createAlternativeBillingOnlyReportingDetailsAsync when it is finished. |
---
title: BillingConfigResponseListener
---

## BillingConfigResponseListener

interface BillingConfigResponseListener

Listener for the result of the getBillingConfigAsync API. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for BillingConfigResponseListener](https://developer.android.com/reference/com/android/billingclient/api/BillingConfigResponseListener).

### Functions

| Name | Summary |
|---|---|
| onBillingConfigResponse | abstract fun onBillingConfigResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/), billingConfig: [BillingConfig](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-config/))<br>Called to notify when the get billing config flow has finished. |
---
title: ExternalOfferInformationDialogListener
---

## ExternalOfferInformationDialogListener

interface ExternalOfferInformationDialogListener

Listener for the result of the [BillingClient.showExternalOfferInformationDialog] API. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for ExternalOfferInformationDialogListener](https://developer.android.com/reference/com/android/billingclient/api/ExternalOfferInformationDialogListener).

### Functions

| Name | Summary |
|---|---|
| onExternalOfferInformationDialogResponse | abstract fun onExternalOfferInformationDialogResponse(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called to notify that the external offer information dialog flow is finished. |
---
title: AlternativeBillingOnlyAvailabilityListener
---

## AlternativeBillingOnlyAvailabilityListener

interface AlternativeBillingOnlyAvailabilityListener

Listener for the result of the isAlternativeBillingOnlyAvailableAsync API. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for AlternativeBillingOnlyAvailabilityListener](https://developer.android.com/reference/com/android/billingclient/api/AlternativeBillingOnlyAvailabilityListener).

### Functions

| Name | Summary |
|---|---|
| onAlternativeBillingOnlyAvailabilityResponse | abstract fun onAlternativeBillingOnlyAvailabilityResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called when a user has selected to make a purchase using alternative billing. |
---
title: AlternativeBillingOnlyInformationDialogListener
---

## AlternativeBillingOnlyInformationDialogListener

interface AlternativeBillingOnlyInformationDialogListener

Listener for the result of the showAlternativeBillingOnlyInformationDialog API. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for AlternativeBillingOnlyInformationDialogListener](https://developer.android.com/reference/com/android/billingclient/api/AlternativeBillingOnlyInformationDialogListener).

### Functions

| Name | Summary |
|---|---|
| onAlternativeBillingOnlyInformationDialogResponse | abstract fun onAlternativeBillingOnlyInformationDialogResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called to notify that the alternative billing only dialog flow is finished. |
---
title: BillingResult
last_updated: 2025-03-19
---

## BillingResult

data class BillingResult(val responseCode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html), val debugMessage: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

Params containing the response code and the debug message from In-app Billing API response.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for BillingResult](https://developer.android.com/reference/com/android/billingclient/api/BillingResult).

### Constructors

| Name | Summary |
|---|---|
| BillingResult | constructor(responseCode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html), debugMessage: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/builder/)<br>Helps to construct BillingResult that are used to return response from In-app Billing API. |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| debugMessage | val debugMessage: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Debug message returned in In-app Billing API calls. |
| responseCode | val responseCode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)<br>Response code returned in In-app Billing API calls. |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [BillingResult.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/builder/) |
---
title: AlternativeBillingOnlyReportingDetails
last_updated: 2025-03-19
---

## AlternativeBillingOnlyReportingDetails

data class AlternativeBillingOnlyReportingDetails(val externalTransactionToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

This class is not used by Meta because Alternative Billing for IAP is not supported.

The details used to report transactions made via alternative billing without user choice to use Google Play billing.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for AlternativeBillingOnlyReportingDetails](https://developer.android.com/reference/com/android/billingclient/api/AlternativeBillingOnlyReportingDetails).

### Constructors

| Name | Summary |
|---|---|
| AlternativeBillingOnlyReportingDetails | constructor(externalTransactionToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Properties

| Name | Summary |
|---|---|
| externalTransactionToken | val externalTransactionToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>An external transaction token that can be used to report a transaction made via alternative billing without user choice to use Google Play billing. |
---
title: AccountIdentifiers
last_updated: 2025-03-19
---

## AccountIdentifiers

data class AccountIdentifiers(val obfuscatedAccountId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val obfuscatedProfileId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

Account identifiers that were specified when the purchase was made.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for AccountIdentifiers](https://developer.android.com/reference/com/android/billingclient/api/AccountIdentifiers).

### Constructors

| Name | Summary |
|---|---|
| AccountIdentifiers | constructor(obfuscatedAccountId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), obfuscatedProfileId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Properties

| Name | Summary |
|---|---|
| obfuscatedAccountId | val obfuscatedAccountId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The obfuscated account id specified in [BillingFlowParams.Builder.setObfuscatedAccountId](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/builder/). |
| obfuscatedProfileId | val obfuscatedProfileId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The obfuscated profile id specified in [BillingFlowParams.Builder.setObfuscatedProfileId](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/builder/). |
---
title: AcknowledgePurchaseResponseListener
---

## AcknowledgePurchaseResponseListener

interface AcknowledgePurchaseResponseListener

Listener for the result of an acknowledge purchase request. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for AcknowledgePurchaseResponseListener](https://developer.android.com/reference/com/android/billingclient/api/AcknowledgePurchaseResponseListener).

### Functions

| Name | Summary |
|---|---|
| onAcknowledgePurchaseResponse | abstract fun onAcknowledgePurchaseResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/))<br>Called to notify that an acknowledge purchase operation has finished. |
---
title: AlternativeChoiceDetails
last_updated: 2025-03-19
---

## AlternativeChoiceDetails

data class ~~AlternativeChoiceDetails~~(val externalTransactionToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val originalExternalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[AlternativeChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/product/)&gt;)

#### Deprecated

Use [BillingClient.Builder.enableUserChoiceBilling] with [UserChoiceBillingListener] and [UserChoiceDetails] in the listener callback instead.

---

Details related to a user's choice of alternative billing.

Alternative Billing for IAP is not supported by Meta.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for AlternativeChoiceDetails](https://developer.android.com/reference/com/android/billingclient/api/AlternativeChoiceDetails).

### Constructors

| Name | Summary |
|---|---|
| AlternativeChoiceDetails | constructor(externalTransactionToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), originalExternalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[AlternativeChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/product/)&gt;) |

### Types

| Name | Summary |
|---|---|
| [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/product/) | data class [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/product/)(val id: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))<br>Details about a product being purchased. |

### Properties

| Name | Summary |
|---|---|
| externalTransactionToken | val externalTransactionToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>A token that represents the user's prospective purchase via alternative billing. |
| originalExternalTransactionId | val originalExternalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The external transaction Id of the originating subscription, if the purchase is a subscription upgrade/downgrade. |
| products | val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[AlternativeChoiceDetails.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/product/)&gt;<br>A list of Product to be purchased in the alternative billing flow. |
---
title: AlternativeBillingListener
---

## AlternativeBillingListener

interface ~~AlternativeBillingListener~~

#### Deprecated

---

Listener interface for the developer-managed alternative billing flow, when it is chosen by the user when initiating a purchase. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for AlternativeBillingListener](https://developer.android.com/reference/com/android/billingclient/api/AlternativeBillingListener).

##### Deprecated

Use enableUserChoiceBilling with  instead.

### Functions

| Name | Summary |
|---|---|
| userSelectedAlternativeBilling | abstract fun userSelectedAlternativeBilling(alternativeChoiceDetails: [AlternativeChoiceDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/alternative-choice-details/))<br>Called when a user has selected to make a purchase using alternative billing. |
---
title: ExternalOfferReportingDetailsListener
---

## ExternalOfferReportingDetailsListener

interface ExternalOfferReportingDetailsListener

Listener for the result of the createExternalOfferReportingDetailsAsync API. 

The equivalent Google Play Billing Library interface can be found at the [Android developer documentation for ExternalOfferReportingDetailsListener](https://developer.android.com/reference/com/android/billingclient/api/ExternalOfferReportingDetailsListener).

### Functions

| Name | Summary |
|---|---|
| onExternalOfferReportingDetailsResponse | abstract fun onExternalOfferReportingDetailsResponse(billingResult: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/), externalOfferReportingDetails: [ExternalOfferReportingDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/external-offer-reporting-details/))<br>Called to receive the results from createExternalOfferReportingDetailsAsync when it is finished. |
---
title: Product
---

## Product

data class Product(val id: String, val offerToken: String, val type: String)

### Constructors

| Name | Summary |
|---|---|
| Product | constructor(id: String, offerToken: String, type: String) |

### Properties

| Name | Summary |
|---|---|
| id | val id: String<br>The id of the product being purchased. |
| offerToken | val offerToken: String<br>Offer token that was passed in BillingClient.launchBillingFlow to purchase the product. |
| type | val type: String<br>The [BillingClient.ProductType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/product-type/) of the product being purchased. |
---
title: BillingConfig
last_updated: 2025-03-19
---

## BillingConfig

data class BillingConfig(val countryCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

BillingConfig stores configuration used to perform billing operations.

Note: This data can change and should not be cached.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for BillingConfig](https://developer.android.com/reference/com/android/billingclient/api/BillingConfig).

### Constructors

| Name | Summary |
|---|---|
| BillingConfig | constructor(countryCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Properties

| Name | Summary |
|---|---|
| countryCode | val countryCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The customer's country code. |
---
title: AgeCategoryResponseListener
last_updated: 2025-03-19
---

## AgeCategoryResponseListener

interface AgeCategoryResponseListener

Listener to Age Category Response.

### Functions

| Name | Summary |
|---|---|
| onQueryAgeCategoryResponse | abstract fun onQueryAgeCategoryResponse(result: [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/), ageCategory: [Integer](https://docs.oracle.com/javase/8/docs/api/java/lang/Integer.html))<br>Called to notify that the query age category operation has finished. |
---
title: AcknowledgePurchaseParams
last_updated: 2025-03-19
---

## AcknowledgePurchaseParams

data class AcknowledgePurchaseParams(val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

Parameters to acknowledge a purchase. See [BillingClient.acknowledgePurchase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/).

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for AcknowledgePurchaseParams](https://developer.android.com/reference/com/android/billingclient/api/AcknowledgePurchaseParams).

### Constructors

| Name | Summary |
|---|---|
| AcknowledgePurchaseParams | constructor(purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/builder/) |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| purchaseToken | val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The token that identifies the purchase to be acknowledged. |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [AcknowledgePurchaseParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/builder/) |
---
title: BillingClient
last_updated: 2025-03-19
---

## BillingClient

abstract class BillingClient

Main interface for communication between the library and user application code.

It provides convenience methods for in-app billing. You can create one instance of this class for your application and use it to process in-app billing operations. It provides synchronous (blocking) and asynchronous (non-blocking) methods for many common in-app billing operations.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for BillingClient](https://developer.android.com/reference/com/android/billingclient/api/BillingClient).

### Constructors

| Name | Summary |
|---|---|
| BillingClient | constructor() |

### Types

| Name | Summary |
|---|---|
| [AgeCategory](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/age-category/) | annotation class [AgeCategory](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/age-category/)<br>Age Category of the user. |
| [BillingResponseCode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/billing-response-code/) | annotation class [BillingResponseCode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/billing-response-code/)<br>Possible response codes. |
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/builder/)<br>Builder to configure and create a BillingClient instance. |
| Companion | object Companion |
| [ConnectionState](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/connection-state/) | annotation class [ConnectionState](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/connection-state/)<br>Connection state of billing client. |
| [FeatureType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/feature-type/) | annotation class [FeatureType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/feature-type/)<br>Features/capabilities supported by isFeatureSupported. |
| [ProductType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/product-type/) | annotation class [ProductType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/product-type/)<br>Supported Product types. |
| [SkuType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/sku-type/) | annotation class [~~SkuType~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/sku-type/)<br>Supported SKU types. |

### Functions

| Name | Summary |
|---|---|
| acknowledgePurchase | abstract fun acknowledgePurchase(params: [AcknowledgePurchaseParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/), listener: &lt;Error class: unknown class&gt;)<br>Acknowledges in-app purchases. |
| consumeAsync | abstract fun consumeAsync(params: [ConsumeParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/consume-params/), listener: &lt;Error class: unknown class&gt;)<br>Consumes a given in-app product. Consuming can only be done on an item that's owned, and as a result of consumption, the user will no longer own it. |
| createAlternativeBillingOnlyReportingDetailsAsync | abstract fun createAlternativeBillingOnlyReportingDetailsAsync(listener: &lt;Error class: unknown class&gt;)<br>Google Play Billing Library allows developers to create alternative billing only purchase details that can be used to report a transaction made via alternative billing without user choice to use Google Play billing. |
| createExternalOfferReportingDetailsAsync | abstract fun createExternalOfferReportingDetailsAsync(listener: &lt;Error class: unknown class&gt;)<br>Creates purchase details that can be used to report a transaction made via external offer. |
| endConnection | abstract fun endConnection()<br>Closes the connection and releases all held resources such as service connections. |
| getBillingConfigAsync | abstract fun getBillingConfigAsync(params: [GetBillingConfigParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/), listener: &lt;Error class: unknown class&gt;)<br>Gets the billing config, which stores configuration used to perform billing operations. |
| getConnectionState | abstract fun getConnectionState(): [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)<br>Get the current billing client connection state. |
| isAlternativeBillingOnlyAvailableAsync | abstract fun isAlternativeBillingOnlyAvailableAsync(listener: &lt;Error class: unknown class&gt;)<br>In the Google Play Billing Library, this checks the availability of offering alternative billing without user choice to use Google Play billing. |
| isExternalOfferAvailableAsync | abstract fun isExternalOfferAvailableAsync(listener: &lt;Error class: unknown class&gt;)<br>Checks the availability of providing external offer. |
| isFeatureSupported | abstract fun isFeatureSupported(feature: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/)<br>Checks if the specified feature or capability is supported. |
| isReady | abstract fun isReady(): [Boolean](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/boolean/index.html)<br>Checks if the client is currently connected to the service, so that requests to other methods will succeed. |
| launchBillingFlow | abstract fun launchBillingFlow(activity: &lt;Error class: unknown class&gt;, params: [BillingFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/)): [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/)<br>Initiates the billing flow for an in-app purchase or subscription. |
| launchPriceChangeConfirmationFlow | abstract fun ~~launchPriceChangeConfirmationFlow~~(activity: &lt;Error class: unknown class&gt;, params: [PriceChangeFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/), listener: &lt;Error class: unknown class&gt;)<br>Launch a price change confirmation flow. |
| queryAgeCategoryAsync | abstract fun queryAgeCategoryAsync(listener: &lt;Error class: unknown class&gt;)<br>Returns the AgeCategory of the user. |
| queryProductDetailsAsync | abstract fun queryProductDetailsAsync(params: [QueryProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/), listener: &lt;Error class: unknown class&gt;)<br>Performs a network query the details of products available for sale in your app. |
| queryPurchaseHistoryAsync | abstract fun ~~queryPurchaseHistoryAsync~~(queryPurchaseHistoryParams: [QueryPurchaseHistoryParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/), listener: &lt;Error class: unknown class&gt;)<br>abstract fun ~~queryPurchaseHistoryAsync~~(skuType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), listener: &lt;Error class: unknown class&gt;)<br>Returns purchases details for items bought within your app. Only the most recent purchase made by the user for each SKU is returned. |
| queryPurchasesAsync | abstract fun queryPurchasesAsync(queryPurchasesParams: [QueryPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchases-params/), listener: &lt;Error class: unknown class&gt;)<br>abstract fun ~~queryPurchasesAsync~~(skuType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), listener: &lt;Error class: unknown class&gt;)<br>Returns purchases details for currently owned items bought within your app. |
| querySkuDetailsAsync | abstract fun ~~querySkuDetailsAsync~~(params: [SkuDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details-params/), listener: &lt;Error class: unknown class&gt;)<br>Performs a network query to get SKU details and return the result asynchronously. |
| showAlternativeBillingOnlyInformationDialog | abstract fun showAlternativeBillingOnlyInformationDialog(activity: &lt;Error class: unknown class&gt;, listener: &lt;Error class: unknown class&gt;): [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/)<br>Shows the alternative billing only information dialog on top of the calling app. |
| showExternalOfferInformationDialog | abstract fun showExternalOfferInformationDialog(activity: &lt;Error class: unknown class&gt;, listener: &lt;Error class: unknown class&gt;): [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/)<br>Shows the external offer information dialog on top of the calling app. |
| showInAppMessages | abstract fun showInAppMessages(activity: &lt;Error class: unknown class&gt;, params: [InAppMessageParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-params/), listener: &lt;Error class: unknown class&gt;): [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/)<br>Overlays billing related messages on top of the calling app. |
| startConnection | abstract fun startConnection(listener: [BillingClientStateListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client-state-listener/))<br>Starts up BillingClient setup process asynchronously. You will be notified through the [BillingClientStateListener](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client-state-listener/) listener when the setup process is complete. |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| connectionState | var connectionState: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) |

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(context: &lt;Error class: unknown class&gt;): [BillingClient.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/builder/) |
---
title: Product
---

## Product

data class Product(val id: String, val offerToken: String, val type: String)

Details about a product being purchased.

### Constructors

| Name | Summary |
|---|---|
| Product | constructor(id: String, offerToken: String, type: String) |

### Properties

| Name | Summary |
|---|---|
| id | val id: String<br>The id of the product being purchased. |
| offerToken | val offerToken: String<br>The id of the product being purchased. |
| type | val type: String<br>The [BillingClient.ProductType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/product-type/) of the product being purchased |
---
title: Builder
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [QueryPurchaseHistoryParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/)<br>Returns an instance of [QueryPurchaseHistoryParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/). |
| setProductType | fun setProductType(productType: String): QueryPurchaseHistoryParams.Builder<br>Set the ProductType to query purchases. |
---
title: BillingFlowParams
last_updated: 2025-03-19
---

## BillingFlowParams

data class BillingFlowParams(val obfuscatedAccountId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null, val obfuscatedProfileId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null, val isOfferPersonalized: [Boolean](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/boolean/index.html) = false, val productDetailsParamsList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[BillingFlowParams.ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/)&gt; = emptyList(), val subscriptionUpdateParams: [BillingFlowParams.SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/)? = null, val skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/)? = null)

Parameters to initiate a purchase flow. See [BillingClient.launchBillingFlow](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/).

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for BillingFlowParams](https://developer.android.com/reference/com/android/billingclient/api/BillingFlowParams).

### Constructors

| Name | Summary |
|---|---|
| BillingFlowParams | constructor(obfuscatedAccountId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null, obfuscatedProfileId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null, isOfferPersonalized: [Boolean](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/boolean/index.html) = false, productDetailsParamsList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[BillingFlowParams.ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/)&gt; = emptyList(), subscriptionUpdateParams: [BillingFlowParams.SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/)? = null, skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/)? = null) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/builder/)<br>Helps to construct BillingFlowParams that are used to initiate a purchase flow. |
| Companion | object Companion |
| [ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/) | data class [ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/)(val productDetails: [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/), val offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null)<br>Params that describe the product to be purchased and the offer to purchase with. |
| [ProrationMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/proration-mode/) | annotation class [~~ProrationMode~~](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/proration-mode/)<br>Replace SKU ProrationMode. |
| [SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/) | class [SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/)(oldPurchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null, externalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null, subscriptionReplacementMode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)? = null)<br>Params that describe a subscription update. |

### Properties

| Name | Summary |
|---|---|
| isOfferPersonalized | val isOfferPersonalized: [Boolean](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/boolean/index.html) = false |
| obfuscatedAccountId | val obfuscatedAccountId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null |
| obfuscatedProfileId | val obfuscatedProfileId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null |
| productDetailsParamsList | val productDetailsParamsList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[BillingFlowParams.ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/)&gt; |
| skuDetails | val ~~skuDetails~~: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/)? = null |
| subscriptionUpdateParams | val subscriptionUpdateParams: [BillingFlowParams.SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/)? = null |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| EXTRA_PARAM_KEY_ACCOUNT_ID | const val EXTRA_PARAM_KEY_ACCOUNT_ID: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) |

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [BillingFlowParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/builder/) |
---
title: Product
---

## Product

data class Product(val productId: String, val productType: String)

A Product identifier used for querying product details.

### Constructors

| Name | Summary |
|---|---|
| Product | constructor(productId: String, productType: String) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/builder/)<br>[Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/builder/) that helps construct Product. |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| productId | val productId: String |
| productType | val productType: String |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [QueryProductDetailsParams.Product.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/builder/)<br>Constructs a new [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/builder/) instance. |
---
title: Builder
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [QueryProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/)<br>Returns an instance of [QueryPurchaseHistoryParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/). |
| setProductList | fun setProductList(productList: List&lt;[QueryProductDetailsParams.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)&gt;): QueryProductDetailsParams.Builder<br>Set the list of [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/). |
---
title: PendingPurchaseUpdate
---

## PendingPurchaseUpdate

data class PendingPurchaseUpdate(val products: List&lt;String&gt;, val purchaseToken: String)

Represents a pending change/update to the existing purchase.

### Constructors

| Name | Summary |
|---|---|
| PendingPurchaseUpdate | constructor(products: List&lt;String&gt;, purchaseToken: String) |

### Properties

| Name | Summary |
|---|---|
| products | val products: List&lt;String&gt;<br>The product ids. |
| purchaseToken | val purchaseToken: String<br>A token that uniquely identifies this pending transaction. |
---
title: PurchaseState
---

## PurchaseState

annotation class PurchaseState

Possible purchase states.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| PENDING | const val PENDING: Int = 2 |
| PURCHASED | const val PURCHASED: Int = 1 |
| UNSPECIFIED_STATE | const val UNSPECIFIED_STATE: Int = 0 |
---
title: Builder
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [AcknowledgePurchaseParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/)<br>Returns [AcknowledgePurchaseParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/) reference to initiate acknowledge action. |
| setPurchaseToken | fun setPurchaseToken(purchaseToken: String): AcknowledgePurchaseParams.Builder<br>Specify the token that identifies the purchase to be acknowledged. |
---
title: Builder
---

## Builder

class ~~Builder~~---

#### Deprecated

This class has been marked as deprecated and removed from Play Billing Library since version 6.0.0.

---

Helps construct [PriceChangeFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/) that are used to launch a price change confirmation flow.

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [PriceChangeFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/)<br>Returns the [PriceChangeFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/) to initiate price change confirmation flow. |
| setSkuDetails | fun setSkuDetails(skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/)): PriceChangeFlowParams.Builder<br>Specifies the SKU that has the pending price change. |
---
title: Builder
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [PendingPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/)<br>Returns [PendingPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/) reference to enable pending purchases. |
| enableOneTimeProducts | fun enableOneTimeProducts(config: String): PendingPurchasesParams.Builder |
| enablePrepaidPlans | fun enablePrepaidPlans(): PendingPurchasesParams.Builder |
---
title: FeatureType
---

## FeatureType

annotation class FeatureType

Features/capabilities supported by isFeatureSupported.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| ALTERNATIVE_BILLING_ONLY | const val ALTERNATIVE_BILLING_ONLY: String<br>Alternative billing only. |
| BILLING_CONFIG | const val BILLING_CONFIG: String<br>Get billing config. |
| EXTERNAL_OFFER | const val EXTERNAL_OFFER: String<br>Play billing library support for external offer. |
| IN_APP_MESSAGING | const val IN_APP_MESSAGING: String<br>Show in-app messages. |
| PRICE_CHANGE_CONFIRMATION | const val PRICE_CHANGE_CONFIRMATION: String<br>Launch a price change confirmation flow. |
| PRODUCT_DETAILS | const val PRODUCT_DETAILS: String<br>Play billing library support for querying and purchasing. |
| SUBSCRIPTIONS | const val SUBSCRIPTIONS: String<br>Purchase/query for subscriptions. |
| SUBSCRIPTIONS_UPDATE | const val SUBSCRIPTIONS_UPDATE: String<br>Subscriptions update/replace. |
---
title: SkuType
---

## SkuType

annotation class ~~SkuType~~

#### Deprecated

Use [ProductType] instead

---

Supported SKU types.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| INAPP | const val INAPP: String<br>A type of SKU for Android apps in-app products. |
| SUBS | const val SUBS: String<br>A type of SKU for Android apps subscriptions. |
---
title: ProductType
---

## ProductType

annotation class ProductType

Supported Product types.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| INAPP | const val INAPP: String<br>A Product type for Android apps in-app products. |
| SUBS | const val SUBS: String<br>A Product type for Android apps subscriptions. |
---
title: InAppMessageResponseCode
---

## InAppMessageResponseCode

annotation class InAppMessageResponseCode

Possible response codes.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| NO_ACTION_NEEDED | const val NO_ACTION_NEEDED: Int = 0<br>The flow has finished and there is no action needed from developers. |
| SUBSCRIPTION_STATUS_UPDATED | const val SUBSCRIPTION_STATUS_UPDATED: Int = 1<br>The subscription status changed. |
---
title: BillingResponseCode
---

## BillingResponseCode

annotation class BillingResponseCode

Possible response codes.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| BILLING_UNAVAILABLE | const val BILLING_UNAVAILABLE: Int = 3<br>A user billing error occurred during processing. |
| DEVELOPER_ERROR | const val DEVELOPER_ERROR: Int = 5<br>Error resulting from incorrect usage of the API. |
| ERROR | const val ERROR: Int = 6<br>Fatal error during the API action. |
| FEATURE_NOT_SUPPORTED | const val FEATURE_NOT_SUPPORTED: Int<br>The requested feature is not supported by the Store on the current device. |
| ITEM_ALREADY_OWNED | const val ITEM_ALREADY_OWNED: Int = 7<br>The purchase failed because the item is already owned. |
| ITEM_NOT_OWNED | const val ITEM_NOT_OWNED: Int = 8<br>Requested action on the item failed since it is not owned by the user. |
| ITEM_UNAVAILABLE | const val ITEM_UNAVAILABLE: Int = 4<br>The requested product is not available for purchase. |
| NETWORK_ERROR | const val NETWORK_ERROR: Int = 12<br>A network error occurred during the operation. |
| OK | const val OK: Int = 0<br>Success. |
| SERVICE_DISCONNECTED | const val SERVICE_DISCONNECTED: Int<br>The app is not connected to the Store because Platform SDK has not been initialized. |
| SERVICE_TIMEOUT | const val ~~SERVICE_TIMEOUT~~: Int<br>This field is deprecated. |
| SERVICE_UNAVAILABLE | const val SERVICE_UNAVAILABLE: Int = 2<br>The service is currently unavailable. |
| USER_CANCELED | const val USER_CANCELED: Int = 1<br>Transaction was canceled by the user. |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [SkuDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details-params/) |
| setSkusList | fun setSkusList(skusList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;): SkuDetailsParams.Builder |
| setType | fun setType(type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): SkuDetailsParams.Builder |
---
title: AgeCategory
---

## AgeCategory

annotation class AgeCategory

Age Category of the user.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| ADULT | const val ADULT: Int = 3<br>Adult age group for users ages 18 and up (or applicable age in user's region). |
| CHILD | const val CHILD: Int = 1<br>Child age group for users between the ages of 10-12 (or applicable age in user's region). |
| TEEN | const val TEEN: Int = 2<br>Teenage age group for users between the ages of 13-17 (or applicable age in user's region). |
| UNKNOWN | const val UNKNOWN: Int = 0 |
---
title: ConnectionState
---

## ConnectionState

annotation class ConnectionState

Connection state of billing client.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| CLOSED | const val CLOSED: Int = 3<br>This client was already closed and shouldn't be used again. |
| CONNECTED | const val CONNECTED: Int = 2<br>This client is currently connected to billing service. |
| CONNECTING | const val CONNECTING: Int = 1<br>This client is currently in process of connecting to billing service. |
| DISCONNECTED | const val DISCONNECTED: Int = 0<br>This client was not yet connected to billing service or was already closed. |
---
title: Product
last_updated: 2025-03-19
---

## Product

data class Product(val id: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

### Constructors

| Name | Summary |
|---|---|
| Product | constructor(id: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Properties

| Name | Summary |
|---|---|
| id | val id: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The id of the product being purchased. |
| offerToken | val offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Offer token that was passed in [BillingClient.launchBillingFlow](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/) to purchase the product. |
| type | val type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The [BillingClient.ProductType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/product-type/) of the product being purchased. |
---
title: OneTimePurchaseOfferDetails
---

## OneTimePurchaseOfferDetails

data class OneTimePurchaseOfferDetails(val formattedPrice: String, val priceAmountMicros: Long, val priceCurrencyCode: String)

Represents the offer details to buy an one-time purchase product.

### Constructors

| Name | Summary |
|---|---|
| OneTimePurchaseOfferDetails | constructor(formattedPrice: String, priceAmountMicros: Long, priceCurrencyCode: String) |

### Properties

| Name | Summary |
|---|---|
| formattedPrice | val formattedPrice: String<br>The formatted price for the payment, including its currency sign. |
| priceAmountMicros | val priceAmountMicros: Long<br>The price for the payment in micro-units, where 1,000,000 micro-units equal one unit of the currency. |
| priceCurrencyCode | val priceCurrencyCode: String<br>ISO 4217 currency code for price. |
---
title: InAppMessageCategoryId
---

## InAppMessageCategoryId

annotation class InAppMessageCategoryId

A high-level category of the in-app message.

One category can be mapped to multiple in-app messages.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| TRANSACTIONAL | const val TRANSACTIONAL: Int = 2<br>The in-app messages of this category are for transactional purpose, such as payment issues. |
| UNKNOWN_IN_APP_MESSAGE_CATEGORY_ID | const val UNKNOWN_IN_APP_MESSAGE_CATEGORY_ID: Int = 0 |
---
title: SubscriptionOfferDetails
---

## SubscriptionOfferDetails

data class SubscriptionOfferDetails(val basePlanId: String, val installmentPlanDetails: [ProductDetails.InstallmentPlanDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/installment-plan-details/), val offerId: String?, val offerTags: List&lt;String&gt;, val offerToken: String, val pricingPhases: [ProductDetails.PricingPhases](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phases/))

Represents the available purchase plans to buy a subscription product.

### Constructors

| Name | Summary |
|---|---|
| SubscriptionOfferDetails | constructor(basePlanId: String, installmentPlanDetails: [ProductDetails.InstallmentPlanDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/installment-plan-details/), offerId: String?, offerTags: List&lt;String&gt;, offerToken: String, pricingPhases: [ProductDetails.PricingPhases](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phases/)) |

### Properties

| Name | Summary |
|---|---|
| basePlanId | val basePlanId: String<br>The base plan id associated with the subscription product. |
| installmentPlanDetails | val installmentPlanDetails: [ProductDetails.InstallmentPlanDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/installment-plan-details/)<br>The additional details of an installment plan. |
| offerId | val offerId: String?<br>The the offer id associated with the subscription product. |
| offerTags | val offerTags: List&lt;String&gt;<br>The offer tags associated with this Subscription Offer. |
| offerToken | val offerToken: String<br>The offer token required to pass in launchBillingFlow to purchase the subscription product with these pricing phases. |
| pricingPhases | val pricingPhases: [ProductDetails.PricingPhases](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phases/)<br>The pricing phases for the subscription product. |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [QueryPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchases-params/)<br>Returns an instance of [QueryPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchases-params/). |
| setProductType | fun setProductType(productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): QueryPurchasesParams.Builder<br>Set the [BillingClient.ProductType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/product-type/) to query purchases. |
---
title: RecurrenceMode
---

## RecurrenceMode

annotation class RecurrenceMode

Recurrence mode of the pricing phase.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| FINITE_RECURRING | const val FINITE_RECURRING: Int = 2<br>The billing plan payment recurs for a fixed number of billing period set in billingCycleCount. |
| INFINITE_RECURRING | const val INFINITE_RECURRING: Int = 1<br>The billing plan payment recurs for infinite billing periods unless cancelled. |
| NON_RECURRING | const val NON_RECURRING: Int = 3<br>The billing plan payment is a one time charge that does not repeat. |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class ~~Builder~~

#### Deprecated

This class has been marked as deprecated and removed from Play Billing Library since version 6.0.0.

---

Helps construct [PriceChangeFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/) that are used to launch a price change confirmation flow.

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [PriceChangeFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/)<br>Returns the [PriceChangeFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/price-change-flow-params/) to initiate price change confirmation flow. |
| setSkuDetails | fun setSkuDetails(skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/)): PriceChangeFlowParams.Builder<br>Specifies the SKU that has the pending price change. |
---
title: InstallmentPlanDetails
---

## InstallmentPlanDetails

data class InstallmentPlanDetails(val installmentPlanCommitmentPaymentsCount: Int, val subsequentInstallmentPlanCommitmentPaymentsCount: Int)

Represents additional details of an installment subscription plan.

### Constructors

| Name | Summary |
|---|---|
| InstallmentPlanDetails | constructor(installmentPlanCommitmentPaymentsCount: Int, subsequentInstallmentPlanCommitmentPaymentsCount: Int) |

### Properties

| Name | Summary |
|---|---|
| installmentPlanCommitmentPaymentsCount | val installmentPlanCommitmentPaymentsCount: Int<br>The committed payments count after a user signs up for this subscription plan. |
| subsequentInstallmentPlanCommitmentPaymentsCount | val subsequentInstallmentPlanCommitmentPaymentsCount: Int<br>The subsequent committed payments count after this subscription plan renews. |
---
title: Builder
---

## Builder

class Builder

Helps construct [InAppMessageParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-params/).

### Functions

| Name | Summary |
|---|---|
| addAllInAppMessageCategoriesToShow | fun addAllInAppMessageCategoriesToShow()<br>Adds all in-app message categories to show. |
| addInAppMessageCategoryToShow | fun addInAppMessageCategoryToShow(inAppMessageCategoryId: Int)<br>Adds a specific in-app message category to show. |
| build | fun build(): [InAppMessageParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-params/)<br>Returns [InAppMessageParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/in-app-message-params/). |
---
title: Builder
---

## Builder

class Builder

Builder to configure and create a [BillingClient](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/) instance.

All methods in the class can be called from any thread, and results will be posted to the same thread.

The equivalent Google Play Billing Library class can be found here: https://developer.android.com/reference/com/android/billingclient/api/BillingClient.Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [BillingClient](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-client/)<br>Creates a Billing client instance. |
| enableAlternativeBillingOnly | fun enableAlternativeBillingOnly(): BillingClient.Builder<br>In the Google Play Billing Library, this enables the ability to offer alternative billing without user choice to use Google Play billing. |
| enableExternalOffer | fun enableExternalOffer(): BillingClient.Builder<br>Enables the ability to offer external offer. |
| enablePendingPurchases | fun ~~enablePendingPurchases~~(): BillingClient.Builder<br>fun enablePendingPurchases(pendingPurchasesParams: [PendingPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/)): BillingClient.Builder<br>Enables pending purchase support. |
| enableUserChoiceBilling | fun enableUserChoiceBilling(userChoiceBillingListener: &lt;Error class: unknown class&gt;): BillingClient.Builder<br>The Google Play Billing Library allows developers to select an alternative billing option during the purchase flow and registers a listener. |
| setAppId | fun setAppId(appId: String): BillingClient.Builder<br>Specifies the AppId for the Quest Apps. |
| setListener | fun setListener(listener: &lt;Error class: unknown class&gt;): BillingClient.Builder<br>Specifies a valid listener for PurchasesUpdatedListener.onPurchasesUpdated events. |
---
title: PricingPhases
---

## PricingPhases

data class PricingPhases(val pricingPhaseList: List&lt;[ProductDetails.PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/)&gt;)

Pricing phases for purchasing an item through a offer. Pricing phases contains time ordered list of [ProductDetails.PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/).

### Constructors

| Name | Summary |
|---|---|
| PricingPhases | constructor(pricingPhaseList: List&lt;[ProductDetails.PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/)&gt;) |

### Properties

| Name | Summary |
|---|---|
| pricingPhaseList | val pricingPhaseList: List&lt;[ProductDetails.PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/)&gt;<br>The pricing phases as a time ordered list of Pricing phase. |
---
title: Builder
---

## Builder

class Builder

Helps construct [GetBillingConfigParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/).

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [GetBillingConfigParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/) |
---
title: PricingPhase
---

## PricingPhase

data class PricingPhase(val billingCycleCount: Int, val billingPeriod: String, val formattedPrice: String, val priceAmountMicros: Long, val priceCurrencyCode: String, val recurrenceMode: Int)

Represents a pricing phase, describing how a user pays at a point in time.

### Constructors

| Name | Summary |
|---|---|
| PricingPhase | constructor(billingCycleCount: Int, billingPeriod: String, formattedPrice: String, priceAmountMicros: Long, priceCurrencyCode: String, recurrenceMode: Int) |

### Properties

| Name | Summary |
|---|---|
| billingCycleCount | val billingCycleCount: Int<br>Number of cycles for which the billing period is applied. |
| billingPeriod | val billingPeriod: String<br>Billing period for which the given price applies, specified in ISO 8601 format. |
| formattedPrice | val formattedPrice: String<br>The formatted price for the payment cycle, including its currency sign. |
| priceAmountMicros | val priceAmountMicros: Long<br>The price for the payment cycle in micro-units, where 1,000,000 micro-units equal one unit of the currency. |
| priceCurrencyCode | val priceCurrencyCode: String<br>ISO 4217 currency code for price. |
| recurrenceMode | val recurrenceMode: Int<br>The [RecurrenceMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/recurrence-mode/) for the pricing phase. |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [ConsumeParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/consume-params/) |
| setPurchaseToken | fun setPurchaseToken(purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): ConsumeParams.Builder |
---
title: Builder
---

## Builder

class Builder

Helps construct [GetBillingConfigParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/).

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [GetBillingConfigParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/get-billing-config-params/) |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [PendingPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/)<br>Returns [PendingPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/) reference to enable pending purchases. |
| enableOneTimeProducts | fun enableOneTimeProducts(config: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): PendingPurchasesParams.Builder |
| enablePrepaidPlans | fun enablePrepaidPlans(): PendingPurchasesParams.Builder |
---
title: PurchaseState
last_updated: 2025-03-19
---

## PurchaseState

annotation class PurchaseState

Possible purchase states.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| PENDING | const val PENDING: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 2 |
| PURCHASED | const val PURCHASED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1 |
| UNSPECIFIED_STATE | const val UNSPECIFIED_STATE: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 0 |
---
title: PricingPhases
last_updated: 2025-03-19
---

## PricingPhases

data class PricingPhases(val pricingPhaseList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[ProductDetails.PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/)&gt;)

Pricing phases for purchasing an item through a offer. Pricing phases contains time ordered list of [ProductDetails.PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/).

### Constructors

| Name | Summary |
|---|---|
| PricingPhases | constructor(pricingPhaseList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[ProductDetails.PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/)&gt;) |

### Properties

| Name | Summary |
|---|---|
| pricingPhaseList | val pricingPhaseList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[ProductDetails.PricingPhase](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phase/)&gt;<br>The pricing phases as a time ordered list of Pricing phase. |
---
title: PendingPurchaseUpdate
last_updated: 2025-03-19
---

## PendingPurchaseUpdate

data class PendingPurchaseUpdate(val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;, val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

Represents a pending change/update to the existing purchase.

### Constructors

| Name | Summary |
|---|---|
| PendingPurchaseUpdate | constructor(products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;, purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Properties

| Name | Summary |
|---|---|
| products | val products: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;<br>The product ids. |
| purchaseToken | val purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>A token that uniquely identifies this pending transaction. |
---
title: RecurrenceMode
last_updated: 2025-03-19
---

## RecurrenceMode

annotation class RecurrenceMode

Recurrence mode of the pricing phase.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| FINITE_RECURRING | const val FINITE_RECURRING: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 2<br>The billing plan payment recurs for a fixed number of billing period set in billingCycleCount. |
| INFINITE_RECURRING | const val INFINITE_RECURRING: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1<br>The billing plan payment recurs for infinite billing periods unless cancelled. |
| NON_RECURRING | const val NON_RECURRING: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 3<br>The billing plan payment is a one time charge that does not repeat. |
---
title: PricingPhase
last_updated: 2025-03-19
---

## PricingPhase

data class PricingPhase(val billingCycleCount: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html), val billingPeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val formattedPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val priceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), val priceCurrencyCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val recurrenceMode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html))

Represents a pricing phase, describing how a user pays at a point in time.

### Constructors

| Name | Summary |
|---|---|
| PricingPhase | constructor(billingCycleCount: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html), billingPeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), formattedPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), priceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), priceCurrencyCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), recurrenceMode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)) |

### Properties

| Name | Summary |
|---|---|
| billingCycleCount | val billingCycleCount: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)<br>Number of cycles for which the billing period is applied. |
| billingPeriod | val billingPeriod: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Billing period for which the given price applies, specified in ISO 8601 format. |
| formattedPrice | val formattedPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The formatted price for the payment cycle, including its currency sign. |
| priceAmountMicros | val priceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html)<br>The price for the payment cycle in micro-units, where 1,000,000 micro-units equal one unit of the currency. |
| priceCurrencyCode | val priceCurrencyCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>ISO 4217 currency code for price. |
| recurrenceMode | val recurrenceMode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)<br>The [RecurrenceMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/recurrence-mode/) for the pricing phase. |
---
title: InAppMessageCategoryId
last_updated: 2025-03-19
---

## InAppMessageCategoryId

annotation class InAppMessageCategoryId

A high-level category of the in-app message.

One category can be mapped to multiple in-app messages.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| TRANSACTIONAL | const val TRANSACTIONAL: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 2<br>The in-app messages of this category are for transactional purpose, such as payment issues. |
| UNKNOWN_IN_APP_MESSAGE_CATEGORY_ID | const val UNKNOWN_IN_APP_MESSAGE_CATEGORY_ID: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 0 |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [QueryPurchaseHistoryParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/)<br>Returns an instance of [QueryPurchaseHistoryParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/). |
| setProductType | fun setProductType(productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): QueryPurchaseHistoryParams.Builder<br>Set the ProductType to query purchases. |
---
title: Product
last_updated: 2025-03-19
---

## Product

data class Product(val productId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

A Product identifier used for querying product details.

### Constructors

| Name | Summary |
|---|---|
| Product | constructor(productId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/builder/)<br>[Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/builder/) that helps construct Product. |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| productId | val productId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) |
| productType | val productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html) |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [QueryProductDetailsParams.Product.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/builder/)<br>Constructs a new [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/builder/) instance. |
---
title: InAppMessageResponseCode
last_updated: 2025-03-19
---

## InAppMessageResponseCode

annotation class InAppMessageResponseCode

Possible response codes.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| NO_ACTION_NEEDED | const val NO_ACTION_NEEDED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 0<br>The flow has finished and there is no action needed from developers. |
| SUBSCRIPTION_STATUS_UPDATED | const val SUBSCRIPTION_STATUS_UPDATED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1<br>The subscription status changed. |
---
title: SubscriptionOfferDetails
last_updated: 2025-03-19
---

## SubscriptionOfferDetails

data class SubscriptionOfferDetails(val basePlanId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val installmentPlanDetails: [ProductDetails.InstallmentPlanDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/installment-plan-details/), val offerId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)?, val offerTags: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;, val offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val pricingPhases: [ProductDetails.PricingPhases](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phases/))

Represents the available purchase plans to buy a subscription product.

### Constructors

| Name | Summary |
|---|---|
| SubscriptionOfferDetails | constructor(basePlanId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), installmentPlanDetails: [ProductDetails.InstallmentPlanDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/installment-plan-details/), offerId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)?, offerTags: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;, offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), pricingPhases: [ProductDetails.PricingPhases](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phases/)) |

### Properties

| Name | Summary |
|---|---|
| basePlanId | val basePlanId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The base plan id associated with the subscription product. |
| installmentPlanDetails | val installmentPlanDetails: [ProductDetails.InstallmentPlanDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/installment-plan-details/)<br>The additional details of an installment plan. |
| offerId | val offerId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)?<br>The the offer id associated with the subscription product. |
| offerTags | val offerTags: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)&gt;<br>The offer tags associated with this Subscription Offer. |
| offerToken | val offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The offer token required to pass in launchBillingFlow to purchase the subscription product with these pricing phases. |
| pricingPhases | val pricingPhases: [ProductDetails.PricingPhases](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/pricing-phases/)<br>The pricing phases for the subscription product. |
---
title: InstallmentPlanDetails
last_updated: 2025-03-19
---

## InstallmentPlanDetails

data class InstallmentPlanDetails(val installmentPlanCommitmentPaymentsCount: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html), val subsequentInstallmentPlanCommitmentPaymentsCount: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html))

Represents additional details of an installment subscription plan.

### Constructors

| Name | Summary |
|---|---|
| InstallmentPlanDetails | constructor(installmentPlanCommitmentPaymentsCount: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html), subsequentInstallmentPlanCommitmentPaymentsCount: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)) |

### Properties

| Name | Summary |
|---|---|
| installmentPlanCommitmentPaymentsCount | val installmentPlanCommitmentPaymentsCount: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)<br>The committed payments count after a user signs up for this subscription plan. |
| subsequentInstallmentPlanCommitmentPaymentsCount | val subsequentInstallmentPlanCommitmentPaymentsCount: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)<br>The subsequent committed payments count after this subscription plan renews. |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [QueryProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/)<br>Returns an instance of [QueryPurchaseHistoryParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-purchase-history-params/). |
| setProductList | fun setProductList(productList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[QueryProductDetailsParams.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)&gt;): QueryProductDetailsParams.Builder<br>Set the list of [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/). |
---
title: SubscriptionUpdateParams
---

## SubscriptionUpdateParams

class SubscriptionUpdateParams(oldPurchaseToken: String? = null, externalTransactionId: String? = null, subscriptionReplacementMode: Int? = null)

Params that describe a subscription update.

### Constructors

| Name | Summary |
|---|---|
| SubscriptionUpdateParams | constructor(oldPurchaseToken: String? = null, externalTransactionId: String? = null, subscriptionReplacementMode: Int? = null) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/builder/)<br>Helps to construct SubscriptionUpdateParams. |
| Companion | object Companion |
| [ReplacementMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/replacement-mode/) | annotation class [ReplacementMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/replacement-mode/)<br>Supported replacement modes to replace an existing subscription with a new one. |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [BillingFlowParams.SubscriptionUpdateParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/builder/)<br>Constructs a new [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/builder/) instance. |
---
title: Builder
---

## Builder

class Builder

Helps to construct [BillingFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/) that are used to initiate a purchase flow.

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [BillingFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/)<br>Returns [BillingFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/) reference to initiate a purchase flow. |
| setIsOfferPersonalized | fun setIsOfferPersonalized(isOfferPersonalized: Boolean): BillingFlowParams.Builder<br>Specifies whether the offer is personalized to the buyer. |
| setObfuscatedAccountId | fun setObfuscatedAccountId(obfuscatedAccountId: String): BillingFlowParams.Builder<br>Specifies an optional obfuscated string that is uniquely associated with the user's account in your app. |
| setObfuscatedProfileId | fun setObfuscatedProfileId(obfuscatedProfileId: String): BillingFlowParams.Builder<br>Specifies an optional obfuscated string that is uniquely associated with the user's profile in your app. |
| setProductDetailsParamsList | fun setProductDetailsParamsList(productDetailsParamsList: List&lt;[BillingFlowParams.ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/)&gt;): BillingFlowParams.Builder<br>Specifies the [ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/) of the items being purchased. |
| setSkuDetails | fun ~~setSkuDetails~~(skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/sku-details/)?): BillingFlowParams.Builder |
| setSubscriptionUpdateParams | fun setSubscriptionUpdateParams(subscriptionUpdateParams: [BillingFlowParams.SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/)): BillingFlowParams.Builder<br>Params used to upgrade or downgrade a subscription. |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

Helps construct [InAppMessageParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-params/).

### Functions

| Name | Summary |
|---|---|
| addAllInAppMessageCategoriesToShow | fun addAllInAppMessageCategoriesToShow()<br>Adds all in-app message categories to show. |
| addInAppMessageCategoryToShow | fun addInAppMessageCategoryToShow(inAppMessageCategoryId: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html))<br>Adds a specific in-app message category to show. |
| build | fun build(): [InAppMessageParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-params/)<br>Returns [InAppMessageParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/in-app-message-params/). |
---
title: ProrationMode
---

## ProrationMode

annotation class ~~ProrationMode~~

#### Deprecated

Use [SubscriptionUpdateParams.ReplacementMode] instead.

---

Replace SKU ProrationMode.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| DEFERRED | const val DEFERRED: Int = 4<br>Replacement takes effect when the old plan expires, and the new price will be charged at the same time. |
| IMMEDIATE_AND_CHARGE_FULL_PRICE | const val IMMEDIATE_AND_CHARGE_FULL_PRICE: Int = 5<br>Replacement takes effect immediately, and the user is charged full price of new plan and is given a full billing cycle of subscription, plus remaining prorated time from the old plan. |
| IMMEDIATE_AND_CHARGE_PRORATED_PRICE | const val IMMEDIATE_AND_CHARGE_PRORATED_PRICE: Int = 2<br>Replacement takes effect immediately, and the billing cycle remains the same. |
| IMMEDIATE_WITH_TIME_PRORATION | const val IMMEDIATE_WITH_TIME_PRORATION: Int = 1<br>Replacement takes effect immediately, and the remaining time will be prorated and credited to the user. |
| IMMEDIATE_WITHOUT_PRORATION | const val IMMEDIATE_WITHOUT_PRORATION: Int = 3<br>Replacement takes effect immediately, and the new price will be charged on next recurrence time. |
| UNKNOWN_SUBSCRIPTION_UPGRADE_DOWNGRADE_POLICY | const val UNKNOWN_SUBSCRIPTION_UPGRADE_DOWNGRADE_POLICY: Int = 0 |
---
title: Builder
---

## Builder

class Builder

Helps to construct [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/) that are used to return response from In-app Billing API.

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-result/) |
| setDebugMessage | fun setDebugMessage(debugMessage: String): BillingResult.Builder |
| setResponseCode | fun setResponseCode(responseCode: Int): BillingResult.Builder |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [AcknowledgePurchaseParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/)<br>Returns [AcknowledgePurchaseParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/acknowledge-purchase-params/) reference to initiate acknowledge action. |
| setPurchaseToken | fun setPurchaseToken(purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): AcknowledgePurchaseParams.Builder<br>Specify the token that identifies the purchase to be acknowledged. |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

Helps to construct [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/) that are used to return response from In-app Billing API.

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [BillingResult](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-result/) |
| setDebugMessage | fun setDebugMessage(debugMessage: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): BillingResult.Builder |
| setResponseCode | fun setResponseCode(responseCode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)): BillingResult.Builder |
---
title: ProductDetailsParams
---

## ProductDetailsParams

data class ProductDetailsParams(val productDetails: [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/), val offerToken: String? = null)

Params that describe the product to be purchased and the offer to purchase with.

### Constructors

| Name | Summary |
|---|---|
| ProductDetailsParams | constructor(productDetails: [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/), offerToken: String? = null) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/builder/)<br>Helps to construct a ProductDetailsParams. |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| offerToken | val offerToken: String? = null |
| productDetails | val productDetails: [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/) |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [BillingFlowParams.ProductDetailsParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/builder/) |
---
title: Product
last_updated: 2025-03-19
---

## Product

data class Product(val id: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

Details about a product being purchased.

### Constructors

| Name | Summary |
|---|---|
| Product | constructor(id: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Properties

| Name | Summary |
|---|---|
| id | val id: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The id of the product being purchased. |
| offerToken | val offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The id of the product being purchased. |
| type | val type: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The [BillingClient.ProductType](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/product-type/) of the product being purchased |
---
title: SkuType
last_updated: 2025-03-19
---

## SkuType

annotation class ~~SkuType~~

#### Deprecated

Use [ProductType] instead

---

Supported SKU types.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| INAPP | const val INAPP: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>A type of SKU for Android apps in-app products. |
| SUBS | const val SUBS: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>A type of SKU for Android apps subscriptions. |
---
title: ProductType
last_updated: 2025-03-19
---

## ProductType

annotation class ProductType

Supported Product types.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| INAPP | const val INAPP: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>A Product type for Android apps in-app products. |
| SUBS | const val SUBS: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>A Product type for Android apps subscriptions. |
---
title: FeatureType
last_updated: 2025-03-19
---

## FeatureType

annotation class FeatureType

Features/capabilities supported by [isFeatureSupported](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/).

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| ALTERNATIVE_BILLING_ONLY | const val ALTERNATIVE_BILLING_ONLY: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Alternative billing only. |
| BILLING_CONFIG | const val BILLING_CONFIG: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Get billing config. |
| EXTERNAL_OFFER | const val EXTERNAL_OFFER: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Play billing library support for external offer. |
| IN_APP_MESSAGING | const val IN_APP_MESSAGING: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Show in-app messages. |
| PRICE_CHANGE_CONFIRMATION | const val PRICE_CHANGE_CONFIRMATION: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Launch a price change confirmation flow. |
| PRODUCT_DETAILS | const val PRODUCT_DETAILS: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Play billing library support for querying and purchasing. |
| SUBSCRIPTIONS | const val SUBSCRIPTIONS: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Purchase/query for subscriptions. |
| SUBSCRIPTIONS_UPDATE | const val SUBSCRIPTIONS_UPDATE: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>Subscriptions update/replace. |
---
title: ConnectionState
last_updated: 2025-03-19
---

## ConnectionState

annotation class ConnectionState

Connection state of billing client.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| CLOSED | const val CLOSED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 3<br>This client was already closed and shouldn't be used again. |
| CONNECTED | const val CONNECTED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 2<br>This client is currently connected to billing service. |
| CONNECTING | const val CONNECTING: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1<br>This client is currently in process of connecting to billing service. |
| DISCONNECTED | const val DISCONNECTED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 0<br>This client was not yet connected to billing service or was already closed. |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

Builder to configure and create a [BillingClient](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/) instance.

All methods in the class can be called from any thread, and results will be posted to the same thread.

The equivalent Google Play Billing Library class can be found at the [Android developer documentation for BillingClient.Builder](https://developer.android.com/reference/com/android/billingclient/api/BillingClient.Builder).

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [BillingClient](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/)<br>Creates a Billing client instance. |
| enableAlternativeBillingOnly | fun enableAlternativeBillingOnly(): BillingClient.Builder<br>In the Google Play Billing Library, this enables the ability to offer alternative billing without user choice to use Google Play billing. |
| enableExternalOffer | fun enableExternalOffer(): BillingClient.Builder<br>Enables the ability to offer external offer. |
| enablePendingPurchases | fun ~~enablePendingPurchases~~(): BillingClient.Builder<br>fun enablePendingPurchases(pendingPurchasesParams: [PendingPurchasesParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/pending-purchases-params/)): BillingClient.Builder<br>Enables pending purchase support. |
| enableUserChoiceBilling | fun enableUserChoiceBilling(userChoiceBillingListener: &lt;Error class: unknown class&gt;): BillingClient.Builder<br>The Google Play Billing Library allows developers to select an alternative billing option during the purchase flow and registers a listener. |
| setAppId | fun setAppId(appId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): BillingClient.Builder<br>Specifies the AppId for the Quest Apps. |
| setListener | fun setListener(listener: &lt;Error class: unknown class&gt;): BillingClient.Builder<br>Specifies a valid listener for PurchasesUpdatedListener.onPurchasesUpdated events. |
---
title: BillingResponseCode
last_updated: 2025-03-19
---

## BillingResponseCode

annotation class BillingResponseCode

Possible response codes.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| BILLING_UNAVAILABLE | const val BILLING_UNAVAILABLE: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 3<br>A user billing error occurred during processing. |
| DEVELOPER_ERROR | const val DEVELOPER_ERROR: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 5<br>Error resulting from incorrect usage of the API. |
| ERROR | const val ERROR: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 6<br>Fatal error during the API action. |
| FEATURE_NOT_SUPPORTED | const val FEATURE_NOT_SUPPORTED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)<br>The requested feature is not supported by the Store on the current device. |
| ITEM_ALREADY_OWNED | const val ITEM_ALREADY_OWNED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 7<br>The purchase failed because the item is already owned. |
| ITEM_NOT_OWNED | const val ITEM_NOT_OWNED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 8<br>Requested action on the item failed since it is not owned by the user. |
| ITEM_UNAVAILABLE | const val ITEM_UNAVAILABLE: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 4<br>The requested product is not available for purchase. |
| NETWORK_ERROR | const val NETWORK_ERROR: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 12<br>A network error occurred during the operation. |
| OK | const val OK: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 0<br>Success. |
| SERVICE_DISCONNECTED | const val SERVICE_DISCONNECTED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)<br>The app is not connected to the Store because Platform SDK has not been initialized. |
| SERVICE_TIMEOUT | const val ~~SERVICE_TIMEOUT~~: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)<br>This field is deprecated. |
| SERVICE_UNAVAILABLE | const val SERVICE_UNAVAILABLE: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 2<br>The service is currently unavailable. |
| USER_CANCELED | const val USER_CANCELED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1<br>Transaction was canceled by the user. |
---
title: AgeCategory
last_updated: 2025-03-19
---

## AgeCategory

annotation class AgeCategory

Age Category of the user.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| ADULT | const val ADULT: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 3<br>Adult age group for users ages 18 and up (or applicable age in user's region). |
| CHILD | const val CHILD: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1<br>Child age group for users between the ages of 10-12 (or applicable age in user's region). |
| TEEN | const val TEEN: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 2<br>Teenage age group for users between the ages of 13-17 (or applicable age in user's region). |
| UNKNOWN | const val UNKNOWN: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 0 |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

Helps to construct [BillingFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/) that are used to initiate a purchase flow.

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [BillingFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/)<br>Returns [BillingFlowParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/) reference to initiate a purchase flow. |
| setIsOfferPersonalized | fun setIsOfferPersonalized(isOfferPersonalized: [Boolean](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/boolean/index.html)): BillingFlowParams.Builder<br>Specifies whether the offer is personalized to the buyer. |
| setObfuscatedAccountId | fun setObfuscatedAccountId(obfuscatedAccountId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): BillingFlowParams.Builder<br>Specifies an optional obfuscated string that is uniquely associated with the user's account in your app. |
| setObfuscatedProfileId | fun setObfuscatedProfileId(obfuscatedProfileId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): BillingFlowParams.Builder<br>Specifies an optional obfuscated string that is uniquely associated with the user's profile in your app. |
| setProductDetailsParamsList | fun setProductDetailsParamsList(productDetailsParamsList: [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin.collections/list/index.html)&lt;[BillingFlowParams.ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/)&gt;): BillingFlowParams.Builder<br>Specifies the [ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/) of the items being purchased. |
| setSkuDetails | fun ~~setSkuDetails~~(skuDetails: [SkuDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/sku-details/)?): BillingFlowParams.Builder |
| setSubscriptionUpdateParams | fun setSubscriptionUpdateParams(subscriptionUpdateParams: [BillingFlowParams.SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/)): BillingFlowParams.Builder<br>Params used to upgrade or downgrade a subscription. |
---
title: ProrationMode
last_updated: 2025-03-19
---

## ProrationMode

annotation class ~~ProrationMode~~

#### Deprecated

Use [SubscriptionUpdateParams.ReplacementMode] instead.

---

Replace SKU ProrationMode.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| DEFERRED | const val DEFERRED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 4<br>Replacement takes effect when the old plan expires, and the new price will be charged at the same time. |
| IMMEDIATE_AND_CHARGE_FULL_PRICE | const val IMMEDIATE_AND_CHARGE_FULL_PRICE: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 5<br>Replacement takes effect immediately, and the user is charged full price of new plan and is given a full billing cycle of subscription, plus remaining prorated time from the old plan. |
| IMMEDIATE_AND_CHARGE_PRORATED_PRICE | const val IMMEDIATE_AND_CHARGE_PRORATED_PRICE: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 2<br>Replacement takes effect immediately, and the billing cycle remains the same. |
| IMMEDIATE_WITH_TIME_PRORATION | const val IMMEDIATE_WITH_TIME_PRORATION: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1<br>Replacement takes effect immediately, and the remaining time will be prorated and credited to the user. |
| IMMEDIATE_WITHOUT_PRORATION | const val IMMEDIATE_WITHOUT_PRORATION: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 3<br>Replacement takes effect immediately, and the new price will be charged on next recurrence time. |
| UNKNOWN_SUBSCRIPTION_UPGRADE_DOWNGRADE_POLICY | const val UNKNOWN_SUBSCRIPTION_UPGRADE_DOWNGRADE_POLICY: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 0 |
---
title: ProductDetailsParams
last_updated: 2025-03-19
---

## ProductDetailsParams

data class ProductDetailsParams(val productDetails: [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/), val offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null)

Params that describe the product to be purchased and the offer to purchase with.

### Constructors

| Name | Summary |
|---|---|
| ProductDetailsParams | constructor(productDetails: [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/), offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/builder/)<br>Helps to construct a ProductDetailsParams. |
| Companion | object Companion |

### Properties

| Name | Summary |
|---|---|
| offerToken | val offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null |
| productDetails | val productDetails: [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/) |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [BillingFlowParams.ProductDetailsParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/builder/) |
---
title: SubscriptionUpdateParams
last_updated: 2025-03-19
---

## SubscriptionUpdateParams

class SubscriptionUpdateParams(oldPurchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null, externalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null, subscriptionReplacementMode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)? = null)

Params that describe a subscription update.

### Constructors

| Name | Summary |
|---|---|
| SubscriptionUpdateParams | constructor(oldPurchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null, externalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)? = null, subscriptionReplacementMode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)? = null) |

### Types

| Name | Summary |
|---|---|
| [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/builder/) | class [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/builder/)<br>Helps to construct SubscriptionUpdateParams. |
| Companion | object Companion |
| [ReplacementMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/replacement-mode/) | annotation class [ReplacementMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/replacement-mode/)<br>Supported replacement modes to replace an existing subscription with a new one. |

## Companion

object Companion

### Functions

| Name | Summary |
|---|---|
| newBuilder | fun newBuilder(): [BillingFlowParams.SubscriptionUpdateParams.Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/builder/)<br>Constructs a new [Builder](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/builder/) instance. |
---
title: Builder
---

## Builder

class Builder

Builder that helps construct [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/).

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [QueryProductDetailsParams.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)<br>Returns an instance of [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/). |
| setProductId | fun setProductId(productId: String): QueryProductDetailsParams.Product.Builder<br>Sets the product id of the product. |
| setProductType | fun setProductType(productType: String): QueryProductDetailsParams.Product.Builder<br>Set the ProductType to query purchases. |
---
title: Builder
---

## Builder

class Builder

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [ConsumeParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/consume-params/) |
| setPurchaseToken | fun setPurchaseToken(purchaseToken: String): ConsumeParams.Builder |
---
title: OneTimePurchaseOfferDetails
last_updated: 2025-03-19
---

## OneTimePurchaseOfferDetails

data class OneTimePurchaseOfferDetails(val formattedPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), val priceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), val priceCurrencyCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html))

Represents the offer details to buy an one-time purchase product.

### Constructors

| Name | Summary |
|---|---|
| OneTimePurchaseOfferDetails | constructor(formattedPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html), priceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html), priceCurrencyCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)) |

### Properties

| Name | Summary |
|---|---|
| formattedPrice | val formattedPrice: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>The formatted price for the payment, including its currency sign. |
| priceAmountMicros | val priceAmountMicros: [Long](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/long/index.html)<br>The price for the payment in micro-units, where 1,000,000 micro-units equal one unit of the currency. |
| priceCurrencyCode | val priceCurrencyCode: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)<br>ISO 4217 currency code for price. |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

Helps to construct [SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/).

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [BillingFlowParams.SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/) |
| setOldPurchaseToken | fun setOldPurchaseToken(purchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): BillingFlowParams.SubscriptionUpdateParams.Builder<br>Specifies the purchase token that the user is upgrading or downgrading from. |
| setOldSkuPurchaseToken | fun ~~setOldSkuPurchaseToken~~(skuPurchaseToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): BillingFlowParams.SubscriptionUpdateParams.Builder<br>This deprecated API will call set the old purchase token via setOldPurchaseToken. |
| setOriginalExternalTransactionId | fun setOriginalExternalTransactionId(externalTransactionId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): BillingFlowParams.SubscriptionUpdateParams.Builder<br>If the originating transaction for the subscription that the user is upgrading or downgrading from was processed via alternative billing, specifies the external transaction id of the originating subscription. |
| setReplaceProrationMode | fun ~~setReplaceProrationMode~~(prorationMode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)): BillingFlowParams.SubscriptionUpdateParams.Builder<br>This deprecated API will set the equivalent [ReplacementMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/replacement-mode/) via setSubscriptionReplacementMode. If the proration mode is not supported, it will default to ReplacementMode.UNKNOWN_REPLACEMENT_MODE. |
| setReplaceSkusProrationMode | fun ~~setReplaceSkusProrationMode~~(prorationMode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)): BillingFlowParams.SubscriptionUpdateParams.Builder<br>This deprecated API will set the equivalent [ReplacementMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/replacement-mode/) via setSubscriptionReplacementMode. If the proration mode is not supported, it will default to ReplacementMode.UNKNOWN_REPLACEMENT_MODE. |
| setSubscriptionReplacementMode | fun setSubscriptionReplacementMode(subscriptionReplacementMode: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html)): BillingFlowParams.SubscriptionUpdateParams.Builder<br>Specifies the ReplacementMode for replacement. |
---
title: Builder
---

## Builder

class Builder

Helps to construct [SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/).

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [BillingFlowParams.SubscriptionUpdateParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/) |
| setOldPurchaseToken | fun setOldPurchaseToken(purchaseToken: String): BillingFlowParams.SubscriptionUpdateParams.Builder<br>Specifies the purchase token that the user is upgrading or downgrading from. |
| setOldSkuPurchaseToken | fun ~~setOldSkuPurchaseToken~~(skuPurchaseToken: String): BillingFlowParams.SubscriptionUpdateParams.Builder<br>This deprecated API will call set the old purchase token via setOldPurchaseToken. |
| setOriginalExternalTransactionId | fun setOriginalExternalTransactionId(externalTransactionId: String): BillingFlowParams.SubscriptionUpdateParams.Builder<br>If the originating transaction for the subscription that the user is upgrading or downgrading from was processed via alternative billing, specifies the external transaction id of the originating subscription. |
| setReplaceProrationMode | fun ~~setReplaceProrationMode~~(prorationMode: Int): BillingFlowParams.SubscriptionUpdateParams.Builder<br>This deprecated API will set the equivalent [ReplacementMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/replacement-mode/) via setSubscriptionReplacementMode. If the proration mode is not supported, it will default to ReplacementMode.UNKNOWN_REPLACEMENT_MODE. |
| setReplaceSkusProrationMode | fun ~~setReplaceSkusProrationMode~~(prorationMode: Int): BillingFlowParams.SubscriptionUpdateParams.Builder<br>This deprecated API will set the equivalent [ReplacementMode](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/subscription-update-params/replacement-mode/) via setSubscriptionReplacementMode. If the proration mode is not supported, it will default to ReplacementMode.UNKNOWN_REPLACEMENT_MODE. |
| setSubscriptionReplacementMode | fun setSubscriptionReplacementMode(subscriptionReplacementMode: Int): BillingFlowParams.SubscriptionUpdateParams.Builder<br>Specifies the ReplacementMode for replacement. |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

Helps to construct a [ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/).

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [BillingFlowParams.ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/) |
| setOfferToken | fun setOfferToken(offerToken: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): BillingFlowParams.ProductDetailsParams.Builder<br>Specifies the identifier of the offer to initiate purchase with. Do not call this method for One-time products. |
| setProductDetails | fun setProductDetails(productDetails: [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/product-details/)): BillingFlowParams.ProductDetailsParams.Builder<br>Specifies the details of item to be purchased, fetched via [BillingClient.queryProductDetailsAsync](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/billing-client/). |
---
title: ReplacementMode
last_updated: 2025-03-19
---

## ReplacementMode

annotation class ReplacementMode

Supported replacement modes to replace an existing subscription with a new one.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| CHARGE_FULL_PRICE | const val CHARGE_FULL_PRICE: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 5<br>The new plan takes effect immediately, and the user is charged full price of new plan and is given a full billing cycle of subscription, plus remaining prorated time from the old plan. |
| CHARGE_PRORATED_PRICE | const val CHARGE_PRORATED_PRICE: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 2<br>The new plan takes effect immediately, and the billing cycle remains the same. |
| DEFERRED | const val DEFERRED: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 6<br>The new purchase takes effect immediately, the new plan will take effect when the old item expires. |
| UNKNOWN_REPLACEMENT_MODE | const val UNKNOWN_REPLACEMENT_MODE: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 0 |
| WITH_TIME_PRORATION | const val WITH_TIME_PRORATION: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 1 |
| WITHOUT_PRORATION | const val WITHOUT_PRORATION: [Int](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/int/index.html) = 3<br>The new plan takes effect immediately, and the new price will be charged on next recurrence time. |
---
title: Builder
last_updated: 2025-03-19
---

## Builder

class Builder

Builder that helps construct [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/).

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [QueryProductDetailsParams.Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/)<br>Returns an instance of [Product](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.1.0/root/com.meta.horizon.billingclient.api/query-product-details-params/product/). |
| setProductId | fun setProductId(productId: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): QueryProductDetailsParams.Product.Builder<br>Sets the product id of the product. |
| setProductType | fun setProductType(productType: [String](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin-stdlib/kotlin/string/index.html)): QueryProductDetailsParams.Product.Builder<br>Set the ProductType to query purchases. |
---
title: Builder
---

## Builder

class Builder

Helps to construct a [ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/).

### Functions

| Name | Summary |
|---|---|
| build | fun build(): [BillingFlowParams.ProductDetailsParams](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/billing-flow-params/product-details-params/) |
| setOfferToken | fun setOfferToken(offerToken: String): BillingFlowParams.ProductDetailsParams.Builder<br>Specifies the identifier of the offer to initiate purchase with. Do not call this method for One-time products. |
| setProductDetails | fun setProductDetails(productDetails: [ProductDetails](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/root/com.meta.horizon.billingclient.api/product-details/)): BillingFlowParams.ProductDetailsParams.Builder<br>Specifies the details of item to be purchased, fetched via BillingClient.queryProductDetailsAsync. |
---
title: ReplacementMode
---

## ReplacementMode

annotation class ReplacementMode

Supported replacement modes to replace an existing subscription with a new one.

### Types

| Name | Summary |
|---|---|
| Companion | object Companion |

## Companion

object Companion

### Properties

| Name | Summary |
|---|---|
| CHARGE_FULL_PRICE | const val CHARGE_FULL_PRICE: Int = 5<br>The new plan takes effect immediately, and the user is charged full price of new plan and is given a full billing cycle of subscription, plus remaining prorated time from the old plan. |
| CHARGE_PRORATED_PRICE | const val CHARGE_PRORATED_PRICE: Int = 2<br>The new plan takes effect immediately, and the billing cycle remains the same. |
| DEFERRED | const val DEFERRED: Int = 6<br>The new purchase takes effect immediately, the new plan will take effect when the old item expires. |
| UNKNOWN_REPLACEMENT_MODE | const val UNKNOWN_REPLACEMENT_MODE: Int = 0 |
| WITH_TIME_PRORATION | const val WITH_TIME_PRORATION: Int = 1 |
| WITHOUT_PRORATION | const val WITHOUT_PRORATION: Int = 3<br>The new plan takes effect immediately, and the new price will be charged on next recurrence time. |

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/horizon-billing-compatibility-sdk.md
---
title: Integrate Meta Horizon Billing Compatibility SDK
description: Explains how to use the Meta Horizon Billing Compatibility SDK.
last_updated: 2024-11-04
---

If you have an existing Android app that is integrated with the [Google Play Billing Library](https://developer.android.com/google/play/billing), you can use the Meta Horizon Billing Compatibility SDK to port your app to the Meta Horizon Store with minimal changes (though there are [known limitations](/documentation/spatial-sdk/horizon-billing-known-limitations)). The SDK supports consumable, durable, and subscription in-app purchases (IAP). The Meta Horizon Billing Compatibility SDK is compatible with the Google Play Billing Library version 7.0.

## Step 1. Add the SDK to your app

Android Platform SDK is deployed to [Maven Central](https://central.sonatype.com/artifact/com.meta.horizon.platform.ovr/android-platform-sdk) so it can be added to your app. In this step, you will add it to your project by editing `app/build.gradle.kts` to include the correct dependencies.

If your app uses Groovy (`build.gradle` instead of `build.gradle.kts`), read the [build dependencies](https://developer.android.com/build/dependencies#add-dependency) page for Groovy syntax.

1. In `app/build.gradle.kts`, create a variable for the Android Platform SDK version above the `dependencies` block:

    ```kotlin
    val androidPlatformSdkVersion = "72"
    val horizonBillingCompatibilitySdkVersion = "1.1.0"
	```

2. At the end of the `dependencies` block, add the following package:

    ```kotlin
    implementation("com.meta.horizon.platform.ovr:android-platform-sdk:$androidPlatformSdkVersion")
	implementation("com.meta.horizon.billingclient.api:horizon-billing-compatibility:$horizonBillingCompatibilitySdkVersion")
    ```

    The variable declaration and `dependencies` block should now look like this:

    ```kotlin
    val androidPlatformSdkVersion = "72"

    dependencies {
    ...
    implementation("com.meta.horizon.platform.ovr:android-platform-sdk:$androidPlatformSdkVersion")
	implementation("com.meta.horizon.billingclient.api:horizon-billing-compatibility:$horizonBillingCompatibilitySdkVersion")
    }
    ```

3. Sync your project with Gradle to download the packages.

    ![GIF of the Gradle sync icon being clicked](/images/fa_aether_tutorial_start_syncgradle.gif)

## Step 2. Add Kotlin support

Meta Horizon Billing Compatibility SDK is implemented in Kotlin and requires consuming apps to include the kotlin stdlib as a dependency. Android apps that have already integrated Kotlin may skip this step.

1. Open your project folder's build.gradle file and add the kotlin-gradle-plugin:
```
	buildscript {
    	dependencies {
        	classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:1.8.22"
    	}
    }
```

2. Open your app folder's build.gradle file and apply the kotlin-android plugin:
```
    apply plugin: 'kotlin-android'
```
3. Add a dependency on `org.jetbrains.kotlin:kotlin-stdlib-jdk7`. For example:
```
	dependencies {
		implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk7:1.8.22"
	}
```
4. Sync your project by selecting **Sync Now** at the top of your build.gradle file in your IDE.

## Step 3. Update import statements

Update Google Play Billing imports in your app's codebase to use Meta Horizon Billing Compatibility SDK imports by replacing all instances of the `com.android.billingclient.api` prefix with the prefix `com.meta.horizon.billingclient.api`.

If any Meta Horizon Billing Compatibility SDK import statement is unresolved, that indicates it isn't supported by the Meta Horizon Billing Compatibility SDK. Remove or modify its usage in the app to make it work with the Meta Horizon Store.


## Step 4. Port Product Catalog from Google Play Store to Meta Horizon Store

Keep the SKUs for the in-app items on the Meta Horizon Developer Center the same as the product IDs on Google Play Console for the app. Otherwise, you will have to update the product IDs in your app as well.

You can follow the instructions available in [Setting Up Add-Ons](/resources/add-ons-setup) for more details on creating your Subscriptions, Consumables and Durables.

## Step 5. Integrate User Age Category

Effective January 2024, for an app to be listed on the Meta Horizon Store, app owners are required to [self-certify](/resources/age-groups/) the intended user age group for their apps. Additionally, if your app is designed for mixed ages  (under 13 or applicable age in user’s region, and 13+), you're required to integrate the [Get Age Category API](/documentation/spatial-sdk/ps-get-age-category-api). By complying with these requirements, you will meet the necessary criteria for listing your app on the Meta Horizon Store.

Integration of the User Age Category API requires use of the Platform SDK for Android.

You can use the `queryAgeCategoryAsync` method in the `BillingClient` class to get the user age category.

```
billingClient.queryAgeCategoryAsync(ageCategoryResponseListenerImpl)
```

Here is the `AgeCategoryResponseListener` that should be implemented.

```
public interface AgeCategoryResponseListener {
  // Called to notify that the query age category operation has finished.
  public void onQueryAgeCategoryResponse(
      BillingResult billingResult, @BillingClient.AgeCategory Integer ageCategory);
}
```

Here is an example implementation of `AgeCategoryResponseListener`.

```
public class AgeCategoryResponseListenerImpl implements AgeCategoryResponseListener {
  void onQueryAgeCategoryResponse(
      BillingResult billingResult, @BillingClient.AgeCategory Integer ageCategory) {
    if (billingResult.getResponseCode() != BillingResponseCode.OK) {
      // handle error
      return;
    }
    switch (ageCategory) {
      case CHILD:
        // handle children (10-12, or applicable age in user's region)
        break;
      case TEEN:
        // handle teens (13-17, or applicable age in user's region)
        break;
      case ADULT:
        // handle adults (18+, or applicable age in user's region)
        break;
      case UNKNOWN:
        // handle case where we don't know the age
        break;
    }
  }
}
```

## Next steps
* Complete [Implement the Google Play Billing Interface](/documentation/spatial-sdk/horizon-billing-implement-google-play-billing-interface/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/horizon-billing-implement-google-play-billing-interface.md
---
title: Implement the Google Play Billing Interface
description: Explains how to implement the Google Play Billing Interface for the Meta Horizon Billing Compatibility SDK.
last_updated: 2024-11-04
---

This page explains how your app can implement in-app purchasing using the Meta Horizon Billing Compatibility SDK. If you've already integrated your app with Google Play Billing Library, you'll make minimal or no code changes in most steps.

For a detailed API reference, see the SDK's [API reference](/documentation/spatial-sdk/horizon-billing-compatibility/api-reference/1.0.0/).

## Before you begin
* Complete [Integrate Meta Horizon Billing Compatibility SDK](/documentation/spatial-sdk/horizon-billing-compatibility-sdk/).

## Remove unsupported fields

The following fields that are available in Google Play Billing are not supported in the Meta Horizon Billing Compatibility SDK. Remove references to these fields from your code.

Request fields:

* Account identifiers (Obfuscated Account ID and Obfuscated Profile ID)

Response fields:

* Account identifiers (Obfuscated Account ID and Obfuscated Profile ID)
* Order ID
* Signature
* Acknowledged


## Initialize a BillingClient

Initialize a `BillingClient` instance. A `BillingClient` object enables communication between Meta Horizon Billing Compatibility APIs and your app. The `BillingClient` provides asynchronous convenience methods for many common billing operations.

Like Google Play Billing, it's strongly recommended that you instantiate only one `BillingClient` instance at a time. However, with the Meta Horizon Billing Compatibility SDK, instantiating multiple `BillingClient` instances at a time doesn't result in multiple `PurchasesUpdatedListener` callbacks for a single purchase event. Instead, calls to a specific instantiation of `BillingClient` update the associated `PurchasesUpdatedListener`.
Create a `BillingClient` using the `newBuilder()` method. Ensure you pass in an Activity as the context. To receive updates on purchases, add a listener by calling `setListener()`. Pass a `PurchasesUpdatedListener` object to the `setListener()` method.

The `enablePendingPurchases()` method is only available as a no-op method . It doesn't enable pending purchases, but remains here for compatibility as Google’s library requires its usage.

The following code shows how to initialize a `BillingClient`.

```
  private PurchasesUpdatedListener purchasesUpdatedListener =
      new PurchasesUpdatedListener() {
        @Override
        public void onPurchasesUpdated(BillingResult billingResult, List<Purchase> purchases) {
          // TODO: implement
        }
      };
  private BillingClient billingClient =
      BillingClint.newBuilder(activity)
          .setListener(purchasesUpdatedListener)
          .enablePendingPurchases()
          .build();
```

## Connect to the Meta Horizon Store

You don't need to make code changes here, but the details of what's happening will be explained.

On calling `startConnection()`, the `BillingClientStateListener` typically receives a callback with `BillingResponseCode.OK`. The `onBillingServiceDisconnected()` method is provided as a no-op method, which is never invoked by the Meta Horizon Billing Compatibility SDK.

The following example demonstrates how to connect to the Meta Horizon Store.

```
    billingClient.startConnection(
        new BillingClientStateListener() {
          @Override
          public void onBillingSetupFinished(BillingResult billingResult) {
            if (billingResult.getResponseCode() == BillingResponseCode.OK) {
              // Query products and purchases here.
            } else {
              // The underlying connection may fail...
            }
          }

          @Override
          public void onBillingServiceDisconnected() {
            // This is a no-op method, which is never invoked by the Meta Horizon Billing
            // Compatibility SDK.
          }
        });
```

## Show products available to buy

You don't need to make code changes here.

Before showing products to your users, make sure to query for product details to get localized product information. You can call `queryProductDetailsAsync()` to query for in-app product details.

The only error response codes the Meta Horizon Billing Compatibility SDK returns are `BillingResponseCode.SERVICE_DISCONNECTED`, and `BillingResponseCode.DEVELOPER_ERROR` and `BillingResponseCode.ERROR`. Other error response codes supported by Google Play Billing are available, but are never returned.

### QueryProductDetailsAsync API

You can query for product details with the `queryProductDetailsAsync()` method. This method takes an instance of `QueryProductDetailsParams`. The `QueryProductDetailsParams` object specifies a list of product ID strings you created in the Meta Horizon Developer Center, along with a `ProductType`. For consumables and durables, the `ProductType` is `ProductType.INAPP`. For subscriptions, the `ProductType` is `ProductType.SUBS`.

For subscription products, the API returns a list of subscription offer details, `List<ProductDetails.SubscriptionOfferDetails>`, that contains all offers available to the user. Each offer has a unique offer token, which you can access by using the `getOfferToken()` method. You must pass the offer token when launching the purchase flow. You can access the offer details of a one-time purchase in-app item with the `getOneTimePurchaseOfferDetails()` method of the API response.

To handle the result of the asynchronous operation, the `queryProductDetailsAsync()` method also requires a listener. This listener is your implementation of the `ProductDetailsResponseListener` interface, where you override `onProductDetailsResponse()`. The `onProductDetailsResponse()` method notifies the listener when the product details query finishes, as shown in the following example.

```
    QueryProductDetailsParams queryProductDetailsParams =
        QueryProductDetailsParams.newBuilder()
            .setProductList(
                ImmutableList.of(
                    Product.newBuilder()
                        .setProductId("product_id_example")
                        .setProductType(ProductType.INAPP)
                        .build()))
            .build();
    billingClient.queryProductDetailsAsync(
        queryProductDetailsParams,
        new ProductDetailsResponseListener() {
          public void onProductDetailsResponse(
              BillingResult billingResult, List<ProductDetails> productDetailsList) {
            if (billingResult.getResponseCode() == BillingResponseCode.OK) {
              // Process the returned ProductDetails List
            } else if (billingResult.getResponseCode() == BillingResponseCode.ERROR) {
              // Handle the error response.
            } else if (billingResult.getResponseCode() == BillingResponseCode.DEVELOPER_ERROR) {
              // Handle the developer error response.
              // Typically this is a sign the developer input was incorrect/in a bad format
            } else if (billingResult.getResponseCode()
                == BillingResponseCode.SERVICE_DISCONNECTED) {
              // startConnection() wasn't called on the BillingClient
            } else {
              // Other error codes are available, but are never returned by the
              // Billing Compatibility SDK.
            }
          }
        });
```

Unlike Google Play Billing, `ProductDetails.getTitle()` does not include the app name.

## Launch the purchase flow

You might need to make minimal code changes here.

Unlike Google Play Billing, the Meta Horizon Billing Compatibility SDK allows at most one product in a single purchase. If the list has more than one item, the error `BillingResponseCode.FEATURE_NOT_SUPPORTED` is returned.

For your app to start the purchase flow, call `launchBillingFlow()` from your app's main thread. The `launchBillingFlow()` method takes a `BillingFlowParams` object, which contains a `ProductDetails` object. You can get `ProductDetails` by calling `queryProductDetailsAsync()`. Create a `BillingFlowParams` object by using the `BillingFlowParams.Builder` class. The following example shows how to launch the billing flow.

```
    // An activity reference from which the billing flow is launched
    Activity activity = ...;
    List productDetailsParamsList =
        List.of(
            ProductDetailsParams.newBuilder()
                // Call queryProductDetailsAsync to get productDetails
                .setProductDetails(productDetails)
                .build());
    BillingFlowParams billingFlowParams =
        BillingFlowParams.newBuilder()
            .setProductDetailsParamsList(productDetailsParamsList)
            .build();
    // Launch the billing flow
    BillingResult billingResult = billingClient.launchBillingFlow(activity, billingFlowParams);
```

The following code shows an example of setting an offer token for a purchase. For more details about the offer token, see the [QueryProductDetailsAsync API](https://developer.amazon.com/docs/in-app-purchasing/implement-google-play-billing.html#queryproductdetailsasync-api).

```
    BillingFlowParams billingFlowParams =
        BillingFlowParams.newBuilder()
            .setProductDetailsParamsList(productDetailsParamsList)
            .setOfferToken(offerDetails.getOfferToken())
            .build();
```

When you initialized your `BillingClient`, you used `setLister()` to add your implementation of `PurchasesUpdatedListener` as a listener. This listener overrides the `onPurchasesUpdated()` method, which delivers the result of your purchase. Your implementation of `onPurchasesUpdated()` must handle the possible response codes, as shown in the following example.

```
  @Override
  void onPurchasesUpdated(BillingResult billingResult, List<Purchase> purchases) {
    if (billingResult.getResponseCode() == BillingResponseCode.OK) {
      for (Purchase purchase : purchases) {
        handlePurchase(purchase);
      }
    } else if (billingResult.getResponseCode() == BillingResponseCode.ERROR) {
      // usually denotes an error with the request/backend
    } else if (billingResult.getResponseCode() == BillingResponseCode.DEVELOPER_ERROR) {
      // typically this involves incorrect inputs
    } else if (billingResult.getResponseCode() == BillingResponseCode.SERVICE_DISCONNECTED) {
      // the developer did not call startConnection() on BillingClient first
    } else {
      // Other error codes are available, but typically are not returned
    }
  }
```

The only error response codes the Meta Horizon Billing Compatibility SDK returns are `BillingResponseCode.SERVICE_DISCONNECTED`, and `BillingResponseCode.DEVELOPER_ERROR` and `BillingResponseCode.ERROR`.  Other error response codes supported by Google Play Billing are available, but are never returned.

When a purchase is successful, a purchase token is generated. A purchase token uniquely identifies a purchase and represents the user and the product ID associated with the purchase.

## Process purchases

You might need to make minimal code changes here.

After a user completes a purchase, your app needs to process that purchase. Your app is usually notified of purchases through your `PurchasesUpdatedListener`. However, there are cases where your app uses `queryPurchasesAsync()` to fetch purchases, as described in [Fetch Purchases](#fetch-purchases).

On completing a purchase, your app should give the content to the user. For entitlements, acknowledge delivery of the content using `acknowledgePurchase()`. For consumables, call `consumeAsync()` to acknowledge delivery and mark the item as consumed.

Review these differences between the Meta Horizon Billing API interface and the Google Play Billing Library:
* Calling `acknowledgePurchase()` is a no-op. We have no specific acknowledgement requirements for subscription or durable purchases.
* Developers should only call `consumeAsync()` on consumable items.
* On non-acknowledgement of purchases, users do not automatically receive refunds. This is different from Google Play Billing, where purchases are revoked on non-acknowledgement for three days as detailed in the [Android developer documentation](https://developer.android.com/google/play/billing/integrate#process).

The following example shows how to consume a product using the associated purchase token:

```
  void handlePurchase(Purchase purchase) {
    // Purchase retrieved from queryPurchasesAsync or your PurchasesUpdatedListener.
    if (purchase.getPurchaseState() != PurchaseState.PURCHASED) {
      return;
    }
    // Deliver item to user.
    // Consume item.
    ConsumeParams consumeParams =
        ConsumeParams.newBuilder().setPurchaseToken(purchase.getPurchaseToken()).build();
    ConsumeResponseListener listener =
        new ConsumeResponseListener() {
          @Override
          public void onConsumeResponse(BillingResult billingResult, String purchaseToken) {
            if (billingResult.getResponseCode() == BillingResponseCode.OK) {
              // Handle the success of the consume operation.
            } else if (billingResult.getResponseCode() == BillingResponseCode.ERROR) {
              // Handle the error response.
            } else {
              // handle misc errors...
            }
          }
        };
    billingClient.consumeAsync(consumeParams, listener);
  }
```

## Fetch purchases

You might need to make minimal code changes here.

Although your app is notified of purchases when listening through `PurchasesUpdatedListener`, certain scenarios might cause your app to be unaware of a purchase a user has made. Scenarios where your app could be unaware of purchases are:

* Network issues: A user makes a successful purchase, but their device has a network connection failure before being notified of the purchase through `PurchasesUpdatedListener`.
* Multiple devices: A user buys an item on a device, switches to another device, and expects to see the item they purchased.
* Subscription lifecycle events: Subscription lifecycle events like renewals occur periodically without API calls from the billing client.

You can handle these scenarios by calling `queryPurchasesAsync()` in your `onResume()` method. This ensures all purchases are successfully processed, as described in Process purchases. Unlike Google Play Billing, `queryPurchasesAsync()` makes a network call when the local cache expires, which affects the time it takes for the listener callback to occur. To reduce the call times in the Meta Horizon Billing Compatibility SDK, limit the number of SKUs to 100 in a `queryPurchasesAsync()` call.

The `queryPurchasesAsync()` method returns only purchases for durable and non-consumed consumables and active subscriptions. The following example shows how to fetch a user's in-app purchases:

```
billingClient.queryPurchasesAsync(
    QueryPurchasesParams.newBuilder().setProductType(ProductType.INAPP).build(),
    new PurchasesResponseListener() {
        public void onQueryPurchasesResponse(
            BillingResult billingResult, List<Purchase> purchases) {
        if (billingResult.getResponseCode() == BillingResponseCode.OK) {
            // handle the return purchase listing
        } else if (billingResult.getResponseCode() == BillingResponseCode.ERROR) {
            // Handle the error response from the backend/network
        } else if (billingResult.getResponseCode() == BillingResponseCode.DEVELOPER_ERROR) {
            // typically involves incorrect inputs
        } else {
            // other error types are available, but not typically returned
        }
        }
    });
```

For subscriptions, pass `ProductType.SUBS`, while creating `QueryPurchasesParams` as shown here.

```
QueryPurchasesParams.newBuilder().setProductType(ProductType.SUBS).build()
```

The only error response codes the Appstore Billing Compatibility SDK returns are `BillingResponseCode.SERVICE_DISCONNECTED`, and `BillingResponseCode.DEVELOPER_ERROR` and `BillingResponseCode.ERROR`. Other error response codes supported by Google Play Billing are available, but are never returned.

## Related topics

- [Integrate Meta Horizon Billing Compatibility SDK](/documentation/spatial-sdk/horizon-billing-compatibility-sdk/)
- [Meta Horizon Billing Compatibility SDK Known Limitations](/documentation/spatial-sdk/horizon-billing-known-limitations/)

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/horizon-billing-known-limitations.md
---
title: Known Limitations
description: Lists the known limitations of the Meta Horizon Billing Compatibility SDK.
last_updated: 2025-01-23
---

Meta Horizon Billing Compatibility SDK is generally compatible with the Google Play Billing Library version 7.0. In the latest release (ie. 1.1.0), there are known limitations regarding full compatibility with Google Play.

## Kotlin

* Meta Horizon Billing Compatibility SDK is implemented in Kotlin and integration with this library will require Java Android apps to include kotlin stdlib in the list of dependencies.

## Subscriptions

* Only active subscriptions are returned and they are assumed to be “infinitely” recurring - that is, they are expected to recur until canceled.
* Re-purchasing a subscription that has only one billing period option (for example, monthly or annual) will not result in an `ITEM_ALREADY_OWNED` error. The response will contain a success message but the user will not be charged again.
* Replacement Mode for upgrading or downgrading a subscription is not supported. The ReplacementMode is defaulted to `WITH_TIME_PRORATION` for all upgrades, and to `DEFERRED` for all downgrades.


## Billing Flow

* Only single-item checkout flows are supported. Any attempt to pass in multiple SKUs will return a BillingResult with `BillingResponseCode.FEATURE_NOT_SUPPORTED`.


## Acknowledgement

* There is no client-side acknowledgement of durables and subscriptions. `BillingClient.acknowledgePurchase()` is a no-op


## Purchases

* `Purchase.orderId` is not supported.
* `Purchase.signature` is not supported.


## Purchase History

* `BillingClient.queryPurchaseHistoryAsync()` provides only a partial view of the history. It will include the latest purchase per-SKU, but does not provide canceled subscriptions, or consumed consumables.


## Billing Config

* Billing Configuration is not currently supported.


## Alternative Billing

* Alternative Billing Only is not supported.


## External Offer

* External Offers are not supported.


## In App Messaging

* In App Messaging is not currently supported.

## Other Known Gaps in Previous Releases
- 1.0.0
  - Subscriptions with a single term, or period, are missing the necessary details about the billing cycle period.
  - Subscriptions with Trial periods or introductory offers do not provide that information in the Pricing Phases. Only the “base” subscription period and price are returned.

## Related topics

- [Integrate Meta Horizon Billing Compatibility SDK](/documentation/spatial-sdk/horizon-billing-compatibility-sdk/)
- [Implement the Google Play Billing Interface](/documentation/spatial-sdk/horizon-billing-implement-google-play-billing-interface/)

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/media-view.md
---
title: Media View showcase
description: Learn how to build a media viewing application with Meta Spatial SDK.
last_updated: 2024-09-19
---

**Build a media viewing application with our new Spatial SDK**

Media View is a mixed reality Quest application that shows developers how to build a spatialized media viewing app using the Spatial SDK. One of the key use cases of mixed reality on Quest is the ability to take full advantage of the space around you for content, instead of being confined to a screen or monitor. Additionally, Quest devices excel at viewing media formats that might be difficult to fully enjoy on mobile or desktop, such as panoramic or 360 content. The Media View app demonstrates the concepts and code required to visually organize media content, display various formats of content in space at the same time, and how to integrate with a cloud hosting solution to easily transfer more media content to the headset for viewing.

You can [download the Media View app on the Meta Store](https://www.meta.com/experiences/media-view/8510454682344317/) and [download its project files from GitHub](https://github.com/meta-quest/Meta-Spatial-SDK-Samples/tree/main/Showcases/media_view).

## Loading and handling local media files

![Loading and handling local media files](/images/mediaview-1.gif)

### Why is this important?
In a media viewing application, visually organizing the list of files on a device, loading local files, and displaying local media are all essential functions.

Media View provides robust media handling capabilities, leveraging the Android MediaStore for accessing, managing, and storing media files on the device. This document dives into the details of how Media View interacts with the MediaStore, detects different media types, and manages sample media assets.

### MediaStore interaction

Media View uses the Android MediaStore to access and manage media files on the user's device. The data/gallery module encapsulates the logic for MediaStore interaction, providing a clean separation of concerns.

* **Querying media:**
    * The MediaStoreQueryBuilder class constructs queries for retrieving media files based on specified filters (MediaFilter) and sort options (MediaSortBy).
    * The buildSelection method dynamically generates selection clauses for the MediaStore query, allowing for flexible filtering based on media types and other criteria.
    * The buildSortOrder method constructs the sort order clause based on the selected MediaSortBy option, allowing users to organize their media by date, size, or name.
* **Media type detection:**
    * The MediaStoreFileDto class represents a media file retrieved from the MediaStore. It includes logic to determine the type of media based on file properties like mime type, aspect ratio, dimensions, and bitrate.
    * Methods like isPanorama, isRayban, is360, and isSpatial use heuristics to categorize media files. For example, panoramas are identified based on their aspect ratio exceeding a certain threshold, while 360-degree media are detected based on a 2:1 aspect ratio.
    * Based on these detection methods, the mediaType and mediaFilter properties of MediaStoreFileDto are set, facilitating filtering and presentation in the UI.
* **Saving media:**
    * The DeviceGalleryService class handles the process of saving new media files to the device. The saveMediaFile method utilizes ContentValues to create a new entry in the MediaStore, specifying properties like display name, mime type, and relative path.
    * The method also opens a file descriptor for the new MediaStore entry, allowing data to be written to the associated file using a FileOutputStream. The IS_PENDING flag is used to indicate that the file is still being written. Once the write is complete, the flag is cleared, signifying that the file is available.

### Sample media management

Media View includes sample media assets that can be saved to the user's device, providing an initial set of content to explore. The data/user module is responsible for managing user preferences, including the tracking of whether sample media has been saved.

* **User preferences:**
    * The UserRepository class provides a centralized way to access and modify user preferences.
    * The UserPreferencesService interacts with SharedPreferences to store and retrieve preferences. The isSampleMediaSaved method checks whether the user has previously saved the sample media.
* **Loading sample assets:**
    * The PermissionViewModel handles the process of loading sample assets from the assets folder. This occurs after the user grants storage permissions.
    * Before saving assets, the code checks if a sample media folder exists from a previous installation. If found, it is deleted to avoid conflicts or duplicates.
    * The saveAssetDirectory and saveAssetFile methods recursively iterate through the sample assets in the assets folder, saving each file to the device using the DeviceGalleryService. The setSampleMediaSaved method in UserRepository is called after successful asset saving to update the user's preference.

### Code examples

**MediaStore query builder (MediaStoreQueryBuilder):**
```
fun buildSelection(filter: MediaFilter?): Pair<String?, Array<String>?> {
    return Pair(
        "${MediaStore.Files.FileColumns.MEDIA_TYPE} = ? OR ${MediaStore.Files.FileColumns.MEDIA_TYPE} = ?",
        arrayOf(
            "${MediaStore.Files.FileColumns.MEDIA_TYPE_IMAGE}",
            "${MediaStore.Files.FileColumns.MEDIA_TYPE_VIDEO}"
        ),
    ) // ... Add support for other MediaFilters
}
```

**Media type detection (MediaStoreFileDto):**
```
private fun isPanorama(): Boolean {
    return aspectRatio?.let { it > MediaType.panoramaAspectRatioMin } ?: false
}
```

**Saving media (DeviceGalleryService):**
```
suspend fun saveMediaFile(
    displayFileName: String?,
    mimeType: String?,
    relativeSubPath: String?,
    onWrite: (FileOutputStream) -> Unit
): Boolean {
    // ... ContentValues setup and MediaStore insertion
    contentResolver.openFileDescriptor(mediaUri, "w", null).use { file ->
        // ... Writing data to the FileOutputStream
    }
    // ... Update MediaStore entry to clear IS_PENDING flag
}
```

**Checking for sample media (UserRepository):**
```
fun isSampleMediaSaved(): Boolean {
    return userPreferencesService.isSampleMediaSaved()
}
```

By combining the robust capabilities of the Android MediaStore with custom logic for media type detection and sample asset management, Media View delivers a comprehensive media handling experience. This approach ensures a seamless workflow for accessing, managing, and presenting diverse media content within the immersive mixed reality environment.

## Display media in a compelling way

![Displaying media in a compelling way](/images/mediaview-2.gif)

### Why is this important?

Displaying regular images and videos is straightforward, but displaying panoramic and 360 content can be a much more magical experience in a headset if done correctly.

Media View's immersive experience leverages the Spatial SDK to create a dynamic and interactive environment within the Meta Quest headset. This document details the mechanisms behind panel management, panel configuration, and spatial debugging, highlighting how Media View blends the virtual and real worlds.

### Panel management
Panels are the primary means of displaying content and facilitating user interaction in Media View's immersive environment. They are essentially virtual surfaces that exist in the user's 3D space, capable of displaying images, videos, UI elements, and more.

* **PanelDelegate Interface:**
    * The PanelDelegate interface defines a set of methods for creating, closing, maximizing, minimizing, and otherwise interacting with panels. This interface serves as a contract between the ImmersiveActivity, which manages the immersive environment, and other components that need to interact with panels.
    * Key methods include:
        * openMediaPanel(mediaModel: MediaModel): Creates and displays a panel for viewing a specific media item.
        * closeMediaPanel(mediaId: Long): Closes the panel associated with a given media item ID.
        * maximizeMedia(mediaModel: MediaModel): Maximizes the panel for a given media item, potentially entering an immersive mode where the panel takes up most of the user's view.
        * minimizeMedia(close: Boolean): Minimizes a maximized panel, optionally closing it completely.
        * openUploadPanel(): Creates and displays a panel for uploading media from Google Drive.
        * closeUploadPanel(): Closes the upload panel.
* **ImmersiveActivity Implementation:**
    * The ImmersiveActivity implements the PanelDelegate interface, providing the concrete logic for panel management. It uses the Spatial SDK to create, position, and manipulate panels within the 3D environment.
    * It maintains an entityMap, which maps panel IDs (integers) to their corresponding Entity objects. Entities are fundamental building blocks in the Spatial SDK, representing objects within the 3D scene. This mapping allows ImmersiveActivity to track and manage panels efficiently.

### Panel configuration (PanelConfigOptions)
The PanelConfigOptions class provides a flexible way to customize the appearance and behavior of panels. Key configuration options include:

* **Dimensions (width, height):** Specify the physical dimensions of the panel in meters. This determines the size of the panel as perceived by the user within their 3D space.
* **layerConfig:** Controls the rendering of the panel's quad layer, allowing for adjustments to transparency and other properties.
* **panelShader:** Determines the shader used to render the panel, allowing for visual effects and customizations.
* **alphaMode:** Sets the alpha blending mode for the panel, influencing how it interacts with other objects in the scene.
* **includeGlass:** Adds a glass-like effect to the panel, making it appear more physically present.
* **dpiOverride:** Overrides the DPI setting for the panel, potentially improving text and image rendering quality.
* **sceneMeshCreator:** A lambda function that allows you to create custom scene meshes for the panel. This provides maximum flexibility in defining the panel's shape and geometry.

**Spatial debugging**
Media View includes components for spatial debugging, aiding in the development and testing of interactions within the 3D environment.

* **SpatialDebugComponent:**
    * This component can be attached to entities to provide visual debugging information about their position, rotation, and scale.
    * It offers properties to control how the entity is positioned and oriented relative to the user's head, including axis of rotation, rotation speed, follow speed, and offsets.
* **SpatialDebugSystem:**
    * This system operates on entities that have the SpatialDebugComponent attached.
    * It calculates and applies transformations to these entities, allowing developers to visualize how objects move and interact in the 3D space.
    * It also includes smoothing and interpolation logic to make the debug visualizations more fluid.

### Code examples

**PanelDelegate Interface:**
```
interface PanelDelegate {
    fun openMediaPanel(mediaModel: MediaModel)
    // ... Other panel management methods
}
```

**Panel creation (ImmersiveActivity):**
```
private fun createGalleryActivity(
    ent: Entity,
    distance: Float,
    positionOffset: Vector3
): PanelSceneObject {
    // ... Panel configuration using PanelConfigOptions
    return PanelSceneObject(scene, spatialContext, GalleryActivity::class.java, ent, config)
}
```

**Custom panel mesh (PanelConfigOptions):**

```
sceneMeshCreator = { texture: SceneTexture ->
    val unlitMaterial = SceneMaterial(texture, AlphaMode.OPAQUE, SceneMaterial.UNLIT_SHADER)
    SceneMesh.cylinderSurface(5.0f, 5.0f, 0.7f, unlitMaterial) // Create a cylindrical panel
}
```

**Spatial debugging (SpatialDebugComponent):**

```
class SpatialDebugComponent(
    axis: LookAtAxis = LookAtAxis.Y,
    // ... Other properties
) : ComponentBase() {
    // ... Attribute definitions for controlling debug behavior
}
```

Through these mechanisms, Media View creates a compelling and interactive mixed reality experience. Panel management provides a structured way to display and interact with content, while panel configuration options enable developers to fine-tune the appearance and behavior of panels. Spatial debugging tools aid in the development and testing of the immersive environment, ensuring a polished and engaging user experience.


## Download new media onto the device using Google Drive integration

Viewing sample media is a good starting point, but providing a way for users to get their own content onto the device and into the media viewer is the actual functionality intended for this app. Google Drive is a great example of a cloud storage provider that can be integrated to help users seamlessly transfer files to their headset.

### How it works: The technical deep dive

Media View's Google Drive integration lets users personalize their VR experiences by accessing their own media collections. It's built with security in mind, ensuring user data and privacy are protected. The integration involves these key components:

1. **Google Drive Picker:**
    * A user-friendly, web-based interface provided by Google for selecting files from a user's Google Drive account.
    * Seamlessly hosted within a WebView in Media View's **UploadActivity.kt**, allowing users to browse their Drive files and select the media they want to download.
2. **Custom JavaScript Interface:**
    * Acts as a bridge between the Android code and the JavaScript code executing within the WebView.
    * Enables smooth communication and data exchange between the native app and the Google Drive Picker.
    * Defined by two essential classes:
        * **DriveConfigJavaScriptInterface:** Provides configuration parameters to the Google Drive Picker, including API keys, client ID, and the necessary scopes for accessing Drive files. Here's an example from **DriveConfig.kt**:

        ```
        data class DriveConfig(
        val scopes: String, // Required scopes for Drive API access
        val clientId: String, // Google Cloud Project Client ID
        val apiKey: String,  // Google Cloud Project API key
        val appId: String,  // Google Cloud Project App ID
        )
        ```

        * **DriveJavaScriptInterface:** Handles events triggered by the Google Drive Picker, such as:
            * Successful user authorization
            * File download progress updates
            * Potential errors during the process. This is illustrated in the code snippet from **DriveJavaScriptInterface.k**t:

```
class DriveJavaScriptInterface(
 private val onAuthCompleted: (token: String?) -> Unit, // Callback for successful authorization
    private val onMediaDownloaded: (media: DriveMedia) -> Unit,  // Callback for file download progress
    private val onDownloadFailed: (reason: String) -> Unit,  // Callback for download errors
) {
    @JavascriptInterface
    fun onAccessTokenReceived(token: String?) {
        onAuthCompleted(token)
    }

    @JavascriptInterface
    fun downloadFile(
        // ... file information (ID, base64 data, mime type, etc.)
    ) {
        // ... decode base64 data, create DriveMedia object, and invoke onMediaDownloaded callback
    }

    @JavascriptInterface
    fun onGetFileFailed(reason: String) {
        onDownloadFailed(reason)
    }
}
```

3. **Authorization flow:**
    * When the user opens the Upload Panel, the WebView loads the Google Drive Picker HTML page.
    * The user is securely prompted to sign in to their Google account and grant Media View permission to access their Drive files (using OAuth 2.0).
    * The DriveJavaScriptInterface receives the access token upon successful authorization, enabling the initiation of file downloads.
4. **File download and storage:**
    * The user selects their desired media file(s) from the Google Drive Picker.
    * The Picker communicates the file ID and download URL to the DriveJavaScriptInterface.
    * The native Android code initiates a download request using the URL, receiving the file data in manageable chunks.
    * As data chunks are received, the DriveJavaScriptInterface keeps the user informed by updating the download progress.
    * Downloaded media is securely stored on the device using the DeviceGalleryService.
    * The DeviceGalleryService interacts with the Android MediaStore to create a new MediaStore entry for the downloaded file, expertly handles the writing of data to the file, and sets the appropriate flags to indicate that the file is ready for viewing. This process is shown in **UploadViewModel.kt**:

```
fun onDownload(driveMedia: DriveMedia) = viewModelScope.launch {
    try {
        // Create or get a MediaStore entry for the file
        val (contentValues, uri) = galleryRepository.createMediaFile(
            driveMedia.fileName,
            driveMedia.mimeType,
            null,
            StorageType.GoogleDrive
        )

        // Write downloaded data to the file
        galleryRepository.writeMediaFile(uri!!) { fos ->
            fos.write(driveMedia.blob)
        }

        // ... Update file progress and completion status
    } catch (t: Throwable) {
        // ... Handle download errors
    }
}
```

### Security considerations
Media View's Google Drive integration prioritizes user privacy and data security:

* **Secure Authorization:** Employs the official Google Drive API and OAuth 2.0 for secure user authentication and authorization.
* **Scoped Access:** Requests only the essential scopes (read access to Drive files) to minimize the app's permissions.
* **Token Handling:** Access tokens are handled securely, avoiding storage in plain text or insecure locations.

### Future enhancements
* **Support for Other Cloud Providers:** Expand integration to include popular cloud storage services such as Dropbox, OneDrive, and iCloud, giving users more options.
* **Direct Upload to Google Drive:** Enable users to upload media they capture within the VR environment directly to their Google Drive accounts, streamlining content creation.


### Conclusion
Google Drive integration empowers Media View users to personalize their virtual reality experiences by seamlessly accessing their media collections. It's built on a foundation of security, ensuring the protection of user data and privacy. Media View's modular design allows for future expansion to incorporate other cloud storage providers, further enhancing the app's flexibility and user appeal.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/os-app-spacewarp.md
---
title: App Spacewarp
description: Describes how App Spacewarp works, and how to measure it, in the Oculus OS.
engine: spatial-sdk
last_updated: 2024-08-16
---

{%include graphics-perf-shared/os-app-spacewarp.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/os-compositor-layers.md
---
title: Compositor layers
description: Describes how compositor Layers work, and how to use them, in the Oculus OS.
engine: spatial-sdk
last_updated: 2024-11-06
---

{%include graphics-perf-shared/os-compositor-layers.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/os-compositor.md
---
title: The compositor
description: Describes how the Compositor works in the Oculus OS.
engine: spatial-sdk
last_updated: 2024-12-04
---

{%include graphics-perf-shared/os-compositor.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-account-linking.md
---
title: Account Linking
description: Describes how to link a user's account in your system with their Meta account to provide a seamless user experience.
engine: spatial-sdk
nativepath: /native/ps-account-linking/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
shell: platform
tags:
 - oculus_platform_sdk
 - identity
 - security
last_updated: 2024-10-15
---

{%include platform-shared/ps-account-linking.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-achievements.md
---
title: Achievements
description: Describes how to create and associate achievements with your apps.
nativepath: /native/ps-achievements/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
engine: spatial-sdk
shell: platform
tags:
 - oculus_platform_sdk
 - social
last_updated: 2024-12-18
---

{%include platform-shared/ps-achievements.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-assets.md
---
title: Asset Files to Manage Download Size
description: Describes how you can reduce your app download size
engine: spatial-sdk
nativepath: /native/ps-assets/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
shell: platform
tags:
 - oculus_platform_sdk
last_updated: 2024-12-18
---

{%include platform-shared/ps-assets.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-attestation-api.md
---
title: Meta Quest Attestation API
description: Describes how to utilize the attestation API to authenticate the integrity of applications and devices.
engine: spatial-sdk
nativepath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
unitypath: default # same page name, but in the folder for other platform
shell: platform
tags:
 - oculus_platform_sdk
last_updated: 2024-12-18
---

{%include platform-shared/ps-attestation-api.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-blockingsdk.md
---
title: Blocking
description: Describes how to handle blocking for Unity.
engine: spatial-sdk
nativepath: /native/ps-blockingsdk/
unrealpath: default
unitypath: default
last_updated: 2024-12-09
---

{%include data-use-checkup-note.md %}

## Blocking and Unblocking Users

Blocking is a core safety feature which users expect in multiplayer games and social experiences. Through this platform feature, you, as a developer, can access who users have blocked and allow users to block directly from their app.

The user-block flow can be used to create new blocks with minimal disruption to the app experience. This is useful in a multiplayer or social setting where a user might encounter another player who is abusive. This flow allows you to prompt a user to block a specific other user, which they can choose to confirm or cancel. The user is then brought right back into your app. You can then access this block data to honor all their blocks in your app.

### Launch User Block Flow

`Users.launchBlockFlow(long userID)`

Input:
`long userID`: The ID of the user that the viewer is going to launch the block flow request.

This method deeplinks the viewer into a modal dialog targeting the specified user to be blocked. From the modal, the viewer can select **Block** to block the user and return to the app. Selecting **Cancel** returns the viewer to their app without any block action.
#### Checking Results

After calling the above method, you can check the `LaunchBlockFlowResult` to get the results of the viewer’s actions from the modal. See [Example Code 1](#example-code-1-handling-block-callback-messages) below for how to handle Block callback messages.

- `LaunchBlockFlowResult.GetDidBlock` checks if the viewer selected **Block** from the modal.
- `LaunchBlockFlowResult.GetDidCancel` checks if the viewer canceled or selected **Back** from the modal.

See Table 1 below for examples of how these values can be used.

### Table 1 Block Result Feedback Cases

|Situation|Description|Result Feedback (LaunchBlockFlowResult)|
|---------|------------------|---------------|
|Successful block|The user will view a dialog allowing them to **Block** or **Cancel**.  The user selects **Block** and the block is executed **successfully**.| `GetDidBlock`: true, `GetDidCancel`: false|
|User cancel|The user will view a dialog allowing them to **Block** or **Cancel**. The user selects **Cancel** and returns the viewer to the app.| `GetDidBlock`: false, `GetDidCancel`: true|
|Viewer tries to block someone they blocked previously|The viewer receives a message informing them of the situation and asking whether they would like to unblock the target user. Selecting **Back** returns the viewer to their app.| `GetDidBlock`: false, `GetDidCancel` : true|
| Viewer Tries to block themselves | The viewer receives a message indicating that this is not supported. Selecting  **Back** returns the viewer to their app. | `GetDidBlock`: false, `GetDidCancel` : true|
|The block cannot be sent for some other reason.|The user receives the message "Unable to block. Please check your connection and try again." Selecting **Back** returns the viewer to the app.| `GetDidBlock`: false, `GetDidCancel`: true|

-------

### Launch User Unblock Flow

`Users.launchUnblockFlow(long userID)`

Input:
`long userID`: The ID of the user that the viewer is going to launch the unblock flow request.

This method deeplinks the viewer into a modal dialog targeting the specified user to be unblocked.  From the modal, the viewer can select **Unblock** to unblock the user and return to the app.  Selecting **Cancel** returns the viewer to their app without any unblock action.

#### Checking Results

After calling the above method, you can check the `LaunchUnblockFlowResult` to get the results of the viewer’s actions from the modal. See [Example Code 1](#example-code-1-handling-block-callback-messages) below for how to handle **Block/Unblock** callback messages.

- `LaunchUnblockFlowResult.getDidBlock` checks if the viewer selected **Unblock** from the modal.
- `LaunchUnblockFlowResult.getDidCancel` checks if the viewer canceled or selected **Back** from the modal.

## Example Code 1: Handling Block Callback Messages

```
using Oculus.Platform;

Users.LaunchBlockFlow(UInt64 userID).OnComplete(OnBlockUser);
...

void OnBlockUser(Message<Models.LaunchBlockFlowResult> message) {
  if (message.IsError) {
    Debug.Log("Error when trying to block the user");
    Debug.LogError(message.Data);
  } else {
    Debug.Log("Got result: DidBlock = " + message.Data.DidBlock + " DidCancel = " + message.Data.DidCancel);
  }
}

...
Users.LaunchUnblockFlow(UInt64 userID).OnComplete(OnUnblockUser);
...

void OnUnblockUser(Message<Models.LaunchUnblockFlowResult> message) {
  if (message.IsError) {
    Debug.Log("Error when trying to unblock the user");
    Debug.LogError(message.Data);
  } else {
    Debug.Log("Got result: DidBlock = " + message.Data.DidUnblock + " DidCancel = " + message.Data.DidCancel);
  }
}
```

## Retrieve a List of the User's Blocked Users

To retrieve a list of a user's blocked users, use the method `Users.getBlockedUsers()`.  This method retrieves an array of the current user's blocked user IDs who are also entitled to your app.   See [Example Code 2](#example-code-2-log-blocked-user-ids) below on how to log the blocked user data.

If there are a large number of values being returned, you may need to call `BlockedUserArray.getNextPage()` and paginate the data.

## Example Code 2: Log Blocked User IDs

```
using Oculus.Platform;

    void GetBlockedUsers()
    {
        Users.GetBlockedUsers().OnComplete(OnGetBlockedUsers);
    }

    void OnGetBlockedUsers(Message<Models.BlockedUserList> message)
    {
        Debug.Log("EXTRACTING BLOCKED USER DATA");
        if (message.IsError)
        {
            Debug.Log("Could not get the list of users blocked!");
            Debug.LogError(message.Data);
        }
        else
        {
            foreach (Models.BlockedUser user in message.GetBlockedUserList())
            {
                Debug.Log("Blocked User: " + user.Id);
            }
        }
    }
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-challenges-s2s.md
---
title: Challenges Server to Server APIs
description: Describes how to create and interact with Challenges using Server to Server methods
engine: spatial-sdk
nativepath: /native/ps-challenges-s2s/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
shell: platform
tags:
 - oculus_platform_sdk
 - social
---

{%include platform-shared/ps-challenges-s2s.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-challenges.md
---
title: Challenges
description: Describes how to create and interact with Challenges
engine: spatial-sdk
nativepath: /native/ps-challenges/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
shell: platform
tags:
 - oculus_platform_sdk
 - social
last_updated: 2024-12-18
---

{%include platform-shared/ps-challenges.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-cloud-backup.md
---
title: Cloud Backup
description: Documentation for the Cloud Backups feature.
engine: spatial-sdk
nativepath: /native/ps-cloud-backup/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
shell: platform
tags:
 - oculus_platform_sdk
last_updated: 2024-12-18
---

{%include platform-shared/ps-cloud-backup.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-cross-device-app-groupings.md
---
title: Meta Cross-Device Development with App Groupings
description: The app grouping feature enables cross-device development by sharing platform settings across all apps in a grouping.
engine: spatial-sdk
nativepath: /native/ps-cross-device-app-groupings/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
shell: platform
tags:
 - oculus_platform_sdk
---

{%include platform-shared/ps-cross-device-app-groupings.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-deep-linking.md
---
title: App Deep Linking
description: Describes the deep linking feature and how to add it to your apps.
engine: spatial-sdk
nativepath: /native/ps-deep-linking/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
shell: platform
tags:
 - oculus_platform_sdk
last_updated: 2025-03-31
---


{%include platform-shared/ps-deep-linking.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-developer-posts.md
---
title: Developer Posts
description: Increase user engagement with your apps by using developer announcements
engine: spatial-sdk
nativepath: /native/ps-developer-posts/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
skip: rift
tags:
 - oculus_platform_sdk
last_updated: 2024-12-18
---

{%include platform-shared/ps-developer-posts.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-entitlement-check.md
---
title: Entitlement Check for Store Apps
description: Describes how you check the users entitlement.
engine: spatial-sdk
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
nativepath: /native/ps-entitlement-check/
last_updated: 2025-04-15
shell: platform
tags:
 - oculus_platform_sdk
---

{%include platform-shared/ps-entitlement-check.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-events.md
---
title: Add Events to Meta Horizon Home
description: Describes how you can use the event feature to promote your VR mixers, parties, and tournaments.
engine: spatial-sdk
nativepath: /native/ps-events/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
shell: platform
tags:
 - oculus_platform_sdk
 - engagement
---

{%include platform-shared/ps-events.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-friend-requests-from-apps.md
---
title: Send Friend Requests from Apps - Mobile
description: Describes how you can enable users to send friend requests from your Meta apps.
engine: spatial-sdk
shell: platform
nativepath: /native/ps-friend-requests-from-apps/
unrealpath: default # same page name, but in the folder for other platform
skip:
 - rift
tags:
 - oculus_platform_sdk
last_updated: 2024-12-09
---


{%include platform-shared/ps-friend-requests-from-apps.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-get-age-category-api.md
---
title: Get Age Category API
description: Describes how to utilize the Get Age Category API in Meta Quest apps.
engine: spatial-sdk
nativepath: /native/ps-get-age-category-api/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
shell: platform
tags:
  - oculus_platform_sdk
last_updated: 2024-10-15
---

{%include platform-shared/ps-get-age-category-api.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-get-started.md
---
title: Get Started with Platform Solutions
description: Describes the steps to download and set up the Meta Platform SDK for development with Android.
engine: spatial-sdk
shell: platform
nativepath: /native/pc/ps-get-started/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
last_updated: 2024-10-15
---

{%include platform-shared/ps-get-started.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-iap-s2s.md
---
title: Add-ons Server APIs
description: Describes how to create and interact with In-App Purchases using Server to Server methods
engine: spatial-sdk
nativepath: /native/ps-iap-s2s/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
shell: platform
tags:
 - oculus_platform_sdk
 - revenue
last_updated: 2025-04-15
---

{%include platform-shared/ps-iap-s2s.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-iap-test.md
---
title: Testing Add-ons
description: Describes how to test your add-ons.
engine: spatial-sdk
nativepath: /native/ps-iap-test/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
shell: platform
tags:
 - oculus_platform_sdk
last_updated: 2025-03-27
---

{%include platform-shared/ps-iap-test.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-iap.md
---
title: Add-ons Integration
description: Describes how you can monetize your Meta app with in-app purchases.
engine: spatial-sdk
unrealpath: default # same page name, but in the folder for other platform
unitypath: default # same page name, but in the folder for other platform
nativepath: /native/ps-iap/
shell: platform
tags:
 - oculus_platform_sdk
last_updated: 2024-10-15
---

{%include platform-shared/ps-iap.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-language-packs.md
---
title: Language Packs
description: Describes how you can reduce your app download size
engine: spatial-sdk
shell: platform
unrealpath: default # same page name, but in the folder for other platform
unitypath: default # same page name, but in the folder for other platform
nativepath: /native/ps-language-packs/
skip:
 - go
 - quest
tags:
 - oculus_platform_sdk
last_updated: 2024-12-18
---

{%include platform-shared/ps-language-packs.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-leaderboards-s2s.md
---
title: Leaderboards Server APIs
description: Describes how leaderboards work and how to integrate them in your Meta apps.
engine: spatial-sdk
shell: platform
nativepath: /native/ps-leaderboards-s2s/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
last_updated: 2024-12-18
---

{%include platform-shared/ps-leaderboards-s2s.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-leaderboards.md
---
title: Leaderboards
description: Describes how leaderboards work and how to integrate them in your Meta apps.
engine: spatial-sdk
shell: platform
nativepath: /native/ps-leaderboards/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
last_updated: 2024-12-18
---

{%include platform-shared/ps-leaderboards.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-managed-account-info.md
---
title: Managed Account Information API
description: Describes how to get additional information for managed accounts in Meta apps.
engine: unity
shell: platform
nativepath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
unitypath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
 - social
last_updated: 2024-12-09
---

{%include platform-shared/ps-managed-account-info.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-monetization-overview.md
---
title: Monetization Overview
description: Overview of the Platform SDK Monetization features
engine: spatial-sdk
shell: platform
nativepath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
unitypath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
 - monetization
last_updated: 2024-10-15
---

{%include platform-shared/ps-monetization-overview.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-ownership.md
---
title: User Verification
description: Describes how to integrate user verfication into your apps.
engine: spatial-sdk
shell: platform
unitypath: default # same page name, but in the folder for other platform
unrealpath: /native/ps-ownership/
nativepath: /native/ps-ownership/
tags:
 - oculus_platform_sdk
 - security
last_updated: 2024-12-09
---

{%include platform-shared/ps-ownership.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-platform-intro.md
---
title: Platform Solutions
engine: spatial-sdk
shell: platform
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
nativepath: /native/ps-platform-intro/
tags:
 - oculus_platform_sdk
last_updated: 2024-12-09
---

{%include platform-shared/ps-platform-intro.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-presence.md
---
title: Users, Friends, and Relationships
description: Describes how users and friends work in Meta apps.
engine: spatial-sdk
shell: platform
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
nativepath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
 - social
last_updated: 2024-12-09
---

{%include platform-shared/ps-presence.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-quest-tools-overview.md
---
title: Quest Tools Overview
description: Overview of the Platform SDK Tools features
engine: spatial-sdk
shell: platform
nativepath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
unitypath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
 - tools
last_updated: 2024-12-09
---

{%include platform-shared/ps-quest-tools-overview.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-reference.md
---
title: Reference Content
description: Provides a link to the Platform reference content
engine: spatial-sdk
shell: platform
nativepath: /native/ps-reference/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
---

{%include platform-shared/ps-reference.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-s2s-basics.md
---
title: Server to Server Basics
engine: spatial-sdk
shell: platform
nativepath: /native/ps-s2s-basics/
unrealpath: default # same page name, but in the folder for other platform
unitypath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
last_updated: 2024-12-18
---


{%include platform-shared/ps-s2s-basics.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-security-overview.md
---
title: Security Overview
description: Overview of the Platform SDK Security features
engine: spatial-sdk
shell: platform
nativepath: default # same page name, but in the folder for other platform
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
 - security
last_updated: 2024-12-18
---

{%include platform-shared/ps-security-overview.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-setup.md
---
title: Set Up for Platform Development with Android Apps
engine: spatial-sdk
tags:
 - oculus_platform_sdk
nativepath: /native/ps-setup/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
last_updated: 2024-12-18
---

This guide will walk you through the basics of setting up your Android development environment and initializing the platform.

## Prerequisites
Before you can integrate the Android Platform SDK, you'll need to create an app, get the associated App ID, and use the App ID when configuring your development environment. To create an app, see the information on the [Creating and Managing Apps page](/resources/publish-create-app/).

**Get your App ID from the Developer Dashboard**

1. In your browser, go to the [Meta Quest Developer Dashboard](/manage/).
2. From the left-side navigation, click **My Apps**.
3. Choose your app from the list of apps.
4. From the left-side navigation, click **Development** > **API**.

You'll find your **App ID** in the middle of the **API** page. You'll need your App ID to call the initialization APIs described in the next few sections.

## Import Android Platform SDK

Android Platform SDK is deployed to [Maven Central](https://central.sonatype.com/artifact/com.meta.horizon.platform.ovr/android-platform-sdk) so it can be added to your app. In this step, you will add it to your project by editing `app/build.gradle.kts` to include the correct dependencies.

If your app uses Groovy (`build.gradle` instead of `build.gradle.kts`), read the [build dependencies](https://developer.android.com/build/dependencies#add-dependency) page for Groovy syntax.

1. In `app/build.gradle.kts`, create a variable for the Android Platform SDK version above the `dependencies` block:

    ```kotlin
    val androidPlatformSdkVersion = "71"
    ```

2. At the end of the `dependencies` block, add the following package:

    ```kotlin
    implementation("com.meta.horizon.platform.ovr:android-platform-sdk:$androidPlatformSdkVersion")
    ```

    The variable declaration and `dependencies` block should now look like this:

    ```kotlin
    val androidPlatformSdkVersion = "71"

    dependencies {
    ...

    implementation("com.meta.horizon.platform.ovr:android-platform-sdk:$androidPlatformSdkVersion")
    }
    ```

3. Sync your project with Gradle to download the packages.

    ![GIF of the Gradle sync icon being clicked](/images/fa_aether_tutorial_start_syncgradle.gif)


## Initialize the SDK
The first step to integrating platform features is implementing the initialization function. There are two initialization functions you can call with your App Id. One is synchronous and runs on the thread you initialize on, the other is asynchronous and allows you to perform other functions, including calls to the Platform SDK, while the SDK is initializing. You should use the asynchronous method for better app performance and less state management.

-  Synchronous - `Core.initialize()`
-  Asynchronous - `Core.asyncInitialize()`


For example:

```
import com.meta.horizon.platform.ovr.Core;

Core.asyncInitialize(appID, context);
```

When using the asynchronous call, the SDK is placed in an intermediate initializing state before full initialization. In this initializing state you're able to run other processes, including making calls to asynchronous Platform SDK methods. Requests made to the Platform SDK in the initializing state will be queued and run after the SDK finishes initializing.

### Initialization Best Practices

In order to properly initialize the Platform SDK, follow these recommendations:

* Use `asyncInitialize()` rather than `initialize()` for Android apps. This is important because `asyncInitialize()` does not block the initialization code, which allows your application to load faster. In addition, `asyncInitialize()` does not throw an exception on Android if the initialization failed.
* Surround the platform API initialization code with a try/catch block, and treat any exceptions that are caught as if the entitlement check failed.
* Set the App Id in the AndroidManifest.xml by adding a `<meta-data>` with the key `com.meta.horizon.platform.ovr.OCULUS_APP_ID`, or call `asyncInitialize()` with an explicit `appId` argument. If an initialization method is called without an explicit `appId` argument, the Platform will try to initialize using the `com.meta.horizon.platform.ovr.OCULUS_APP_ID` stored in your

Example `<meta-data>` in your AndroidManifest.xml

```
<meta-data
   android:name="com.meta.horizon.platform.ovr.OCULUS_APP_ID"
   android:value="MY_OCULUS_APP_ID"
/>
```

## Initialize the SDK and Perform the Entitlement Check {#entitlement}
The first step to integrating the SDK is implementing the initialization function, and next you should perform the entitlement check. For instructions on how to do this, see [Entitlement Check](/documentation/native/ps-entitlement-check/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-sharing.md
---
title: Share Content
description: Describes how to enable users to share their VR experiences with their Facebook network with casting, video recording, or photo sharing.
engine: spatial-sdk
shell: platform
nativepath: /native/ps-sharing/
unrealpath: default
unitypath: default
skip:
 - rift
tags:
 - oculus_platform_sdk
---

{%include platform-shared/ps-sharing.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-social-features-overview.md
---
title: Social Features Overview
description: Overview of the Platform SDK Social features
engine: spatial-sdk
shell: platform
nativepath: default # same page name, but in the folder for other platform
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
 - social_features
last_updated: 2024-12-09
---

{%include platform-shared/ps-social-features-overview.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-subscriptions-s2s.md
---
title: Server APIs for Subscriptions
description: Describes how to create and interact with subscriptions using server to server methods
engine: spatial-sdk
shell: platform
unitypath: default
unrealpath: default
unitypath: default
tags:
 - oculus_platform_sdk
 - revenue
last_updated: 2024-10-15
---

{%include platform-shared/ps-subscriptions-s2s.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-system-deep-linking.md
---
title: System Deep Linking
description: Describes adding deep links to system applications to your apps.
engine: spatial-sdk
nativepath: /native/ps-deep-linking/
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
shell: platform
tags:
 - oculus_platform_sdk
last_updated: 2024-12-18
---

{%include platform-shared/ps-system-deep-linking.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-user-engagement-overview.md
---
title: User Engagement Overview
description: Steps to test travel features and use cases.
engine: spatial-sdk
shell: platform
nativepath: default # same page name, but in the folder for other platform
unitypath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
 - engagement
last_updated: 2024-12-18
---

{%include platform-shared/ps-user-engagement-overview.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-user-management-overview.md
---
title: User Management Overview
description: Overview of the Platform SDK User Management features
engine: spatial-sdk
shell: platform
nativepath: default # same page name, but in the folder for other platform
unrealpath: default # same page name, but in the folder for other platform
unitypath: default # same page name, but in the folder for other platform
tags:
 - oculus_platform_sdk
 - user_management
last_updated: 2024-12-18
---

{%include platform-shared/ps-user-management-overview.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-user-notifications-analytics.md
---
title: User Notifications Analytics
description: Describes the user notifications analytics page.
engine: spatial-sdk
shell: platform
nativepath: /native/ps-user-notifications-analytics/
unrealpath: default
unitypath: default
tags:
 - oculus_platform_sdk
last_updated: 2024-12-18
---

{%include platform-shared/ps-user-notifications-analytics.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-user-notifications-create.md
---
title: Create User Notifications
description: Describes how to create user notifications.
engine: spatial-sdk
shell: platform
nativepath: /native/ps-user-notifications-create/
unrealpath: default
unitypath: default
tags:
 - oculus_platform_sdk
last_updated: 2024-12-18
---

{%include platform-shared/ps-user-notifications-create.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-user-notifications-event.md
---
title: Event-based User Notifications
description: Describes how to create and trigger event-based user notifications.
engine: spatial-sdk
shell: platform
nativepath: /native/ps-user-notifications-event/
unrealpath: default
unitypath: default
tags:
 - oculus_platform_sdk
---

{%include platform-shared/ps-user-notifications-event.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-user-notifications.md
---
title: User Notifications Overview
description: Describes User Notifications feature used to contact owners of an app.
engine: spatial-sdk
shell: platform
nativepath: /native/ps-user-notifications/
unitypath: default
unrealpath: default
tags:
 - oculus_platform_sdk
last_updated: 2024-12-18
---

{%include platform-shared/ps-user-notifications.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ps-webhooks-getting-started.md
---
title: "Getting Started with Webhooks"
description: "Provides information to help readers jump into creating webhooks subscriptions."
engine: spatial-sdk
shell: platform
nativepath: /native/ps-webhooks-getting-started/
unitypath: default
unrealpath: default
tags:
 - oculus_platform_sdk
 - social
last_updated: 2025-03-26

{%include platform-shared/ps-webhooks-getting-started.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/release-notes.md
---
title: Meta Spatial SDK Release notes
last_updated: 2025-04-22
hide_table_of_contents: true
---

<br />

<accordion expansion-type="multiple">
<accordion-item is-initially-expanded="true">
<accordion-item-title heading-display-type="mcds_title_small" heading-semantic-type="heading3">
  Apr 22, 2025 — Meta Spatial SDK v0.6.0
</accordion-item-title>
<accordion-item-content markdown="block">

### Added

- Experimental Feature: [Interaction SDK](/documentation/spatial-sdk/spatial-sdk-isdk-overview/)
  - Using `IsdkFeature` automatically replaces built in toolkit components/systems like Grabbable with `Isdk` equivalents
  - Provides interactions that are consistent with the Meta Horizon OS and brings parity between controller and hand interactions
    - Interact with panels directly using hands or controllers
    - Grab 3D objects with hands or controllers, directly or using a raycast
    - Advanced grab customization (responsiveness, two-handed, constraints)
  - The `Object3DSampleIsdk` sample app in the [samples repo](https://github.com/meta-quest/Meta-Spatial-SDK-Samples) demonstrates how to use the new IsdkFeature and other Isdk APIs
- [Datamodel Inspector](/documentation/spatial-sdk/spatial-sdk-tooling-dmi)
  - Using `DataModelInspectorFeature` launches a webserver at a specified port that provides a live table view of ECS.
  - Connect to a running app via Data Model Inspector Tool Window in the new Meta Horizon Android Studio Plugin.
- [Query filters and sorting](/documentation/spatial-sdk/spatial-sdk-queries/)
  - [Add filtering API for queries](/documentation/spatial-sdk/spatial-sdk-filters/) so that developers can refine the entity query results by applying filters on attributes.
  - [Add sorting API for queries](/documentation/spatial-sdk/spatial-sdk-sorting/) so that developers can sort the entity by criteria on attributes.
- GLTF Animation Pointer Support
  - Added the ability to modify material factors and UV transforms via `KHR_animation_pointer` support.
  - This can allow you to do things like animate opacity or make moving textures and play them with the `Animated()` component.
- [DRM support](/documentation/spatial-sdk/spatial-sdk-2dpanel-drm) for Activity based panels on v76
  - Using an Activity based panel (not inflated view) along with a `LayerConfig` set to `secure=true` will allow you to display DRM content on v76+. Previously, you had to render directly to a secure swapchain.

### Changed

- We now support Color4 as an Attribute Type for use directly in components. Because of this, Color4 has been moved packages from `com.meta.spatial.toolkit` -> `com.meta.spatial.core`
- Uris are now supported as an Attribute Type for use in components
- Component XML is now the preferred method for making Spatial SDK Components
  - Using Components XML increases performance of components and queries.
  - Components XML can be used in Spatial Editor.
  - Components written in Kotlin (instead of XML) will no longer be able to be added to objects in Spatial Editor
- `PanelAnimation` and `PanelConfigOptions2` are now marked as experimental
  - These APIs may be unstable and/or subject to change in the future. If you want to use them now, you will need to use the `@SpatialSDKExperimentalAPI` annotation
- Default cursor has been changed to more closely match the Quest Home environment cursor
- Samples now use `libs.versions.toml` for version management (removing the need to set the version in the `gradle.properties` file)
- Changed the behavior of the `Layer.setClip()` API
  - If the area of the clip for the left or right eye is 0, there will be no layer submitted for that eye.
  - This can allow you to have separate transforms for layers sharing a swapchain with the left and right eyes
- Bundled shaders assets have been cleaned up and compressed, decreasing APK size.
- Various performance and stability improvements.

### Fixed

- Fixed bug where deleting an entity while grabbed causes a crash

</accordion-item-content>
</accordion-item>
<accordion-item>
<accordion-item-title heading-display-type="mcds_title_small" heading-semantic-type="heading3">
  Feb 18, 2025 — Meta Spatial SDK v0.5.5
</accordion-item-title>
<accordion-item-content markdown="block">

### Added

- Component XML
  - Components can now be defined in XML instead of Kotlin, this is now the preferred way to write Components
  - This makes it easier to define Components, and greatly improves the Spatial Editor integration with Components
  - The build process will generate Kotlin code and resource files for the XML components
- Panel Animation
  - This new feature includes animation timing and callback APIs, enabling you to manipulate panel transitions seamlessly
  - A panel zoom in and out animation is now available when creating and destroying panels
  - These capabilities enhance the interactivity and aesthetic appeal of your panels, providing you with greater control and flexibility
- Panel Native Transition between Quad and Cylinder Shapes
  - We have implemented animations for transitions between Quad and Cylinder panels
  - Check out the AnimationSample for an example
- Refined Cylinder Panels
  - We have conducted a comprehensive refinement of our Cylinder Panels to deliver enhanced performance and versatility. Key improvements include:
    - Grabbable Bug Fix: We have resolved a bug with Grabbable and cylinder panels, grabbing cylinder panels will now be more reliable
    - Backside Transparency: We have added transparency to the backside of the cylinder panels, staying consistent with quad panels

### Changed

- com.meta.spatial.toolkit.Controller.kt
  - In the Controller class, property “type” is now an EnumAttribute that accepts Enum values of `com.meta.spatial.toolkit.ControllerType`. The ControllerType enum is defined in the Java package ControllerType and has three values: `ControllerType.CONTROLLER`, `ControllerType.HAND`, and `ControllerType.EYES`.
  - The constants `com.meta.spatial.toolkit.Controller.CONTROLLER_TYPE`, `com.meta.spatial.toolkit.Controller.HAND_TYPE`, and `com.meta.spatial.toolkit.Controller.EYES_TYPE` are removed.
- TimeAttribute has changed from Int->Long

### Deprecated

- Writing Components using Kotlin is now deprecated, please shift to using Component XML to define your Components

### Fixed

- Fixed bug with rotation with Locomotion + behavior with updateViewOrigin
- Optimized panel update performance for large panels

</accordion-item-content>
</accordion-item>
<accordion-item>
<accordion-item-title heading-display-type="mcds_title_small" heading-semantic-type="heading3">
  Jan 23, 2025 — Meta Spatial SDK v0.5.4
</accordion-item-title>
<accordion-item-content markdown="block">

### Added

- Added `onHeadsetMounted` and `onHeadsetUnmounted` APIs for detecting when a user puts on or takes off their headset.

### Changed

- None

### Deprecated

- None

### Fixed

- Fixed Windows specific hot reload bug with "Read-only filesystem" error in Gradle task.
- Fixed crash where a `SceneLayer` was being destroyed twice due to garbage collection.
</accordion-item-content>
</accordion-item>
<accordion-item>
<accordion-item-title heading-display-type="mcds_title_small" heading-semantic-type="heading3">
  Dec 16, 2024 — Meta Spatial SDK v0.5.2
</accordion-item-title>
<accordion-item-content markdown="block">

### Added

- The `meta-spatial-sdk-compose` package is now available, enabling View-based panels to render Jetpack Compose UI
- Javadocs are now available for Maven Central released packages (starting with 0.5.3)
- MRUK
  - Added Scene Raycasting functionality (and a raycast demo in the MrukSample project)
  - Optimized scene loading

### Changed

- None

### Deprecated

- None

### Fixed

- Hot reload is now more reliable (previously has issues with parallelization)

</accordion-item-content>
</accordion-item>
<accordion-item>
<accordion-item-title heading-display-type="mcds_title_small" heading-semantic-type="heading3">
  Nov 14, 2024 — Meta Spatial SDK v0.5.2
</accordion-item-title>
<accordion-item-content markdown="block">

### Added

- Added `Followable` Component and `FollowableSystem` which allows devs to easily tether objects together. See Animations Sample for an example use.
- **Hot Reload**: Adds the ability to reload your `glb`/`gltf`/`glxf` and Meta Spatial Editor scenes while running your app via the Gradle plugin.
  - Auto Export from Meta Spatial Editor: Saving in Spatial Editor automatically exports to the app and pushes to the headset for hot reload
  - Two Reload Types:
    - Delete all entities and recreate them: more stable but does not work for all apps
    - Keep entities and reload meshes only: works for all apps, but less stable and does not reload components

### Changed

- `SamplerConfig`s now also apply to layers instead of just non-layer panels
- Cylinder panels now have a transparent back applied to them (instead of just being invisible)
- **Gradle Plugin**: References to string paths in plugin configuration are replaced with file references.
  - **NOTE:** This requires changes to your `build.gradle.kts`. Example new usage can be found in the sample `build.gradle.kts` files.
- **Gradle Plugin**: Telemetry now reports out simple usage statistics.

### Deprecated

- Deprecated `QuadLayerConfig`/`CylinderLayerConfig`/`EquirectLayerConfig`. Use `LayerConfig` instead for panel's layer configuration.

### Fixed

- Fixed a crash when garbage collecting a panel.
- Fixed a crash when updating the `Panel` component on an entity that already had a `Panel` component.
- Crash fixed in Focus showcase

</accordion-item-content>
</accordion-item>
<accordion-item>
<accordion-item-title heading-display-type="title-small" heading-semantic-type="heading3">
  Oct 23, 2024 — Meta Spatial SDK v0.5.1
</accordion-item-title>
<accordion-item-content markdown="block">

### Added

- Added support for Secure layers Layers can now be marked as secure making them appear black while recording. This is possible at a global level or an individual layer level.

```kotlin
// globally enable
scene.setSecureLayers(true)

// individually enable
myLayerConfig.secure = true
```

In addition, this value can be set on a global level using your AndroidManifest

```kotlin
<meta-data
      android:name="com.meta.spatial.SECURE_LAYERS"
      android:value="true"
/>
```

### Removed

- Removed the old Anchor Systems in toolkit, please use MRUK (Mixed Reality Utility Kit) in Meta Spatial SDK

### Fixed

- Init order issue for FeatureManager An overridden registerFeatures() was not able to reference the top level class variables. This was because the initialization was happening very early in the creation of a Feature. This was resolved by moving initialization later in activity startup.
- Memory leak on panel destruction Destroy the activity panel by calling lifecycle events onPause, onStop, onDestroy sequentially. Release the panel scene texture and mesh as panel destruction, which reclaims the resource early.
- Fixed the issue that the panel faced the user backwards when grabbed from behind. The panel will now always face the user correctly, regardless of the angle of grabbing.
- Fix the grabbable bug for the cylinder panel when the user is close to the panel. When the user is very close to the panel, i.e., the center of the cylinder is behind the user, the grabbable system does not work well for rotation.
- Fix compatibility issues with Android Studio Ladybug.

</accordion-item-content>
</accordion-item>
</accordion>

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-asset-library.md
---
title: Asset Library
description: Meta Spatial Editor offers a library of freely available assets that you can use in your own apps.
last_updated: 2025-01-14
---

Spatial Editor offers a library of freely available assets that you can use in your own apps.

## Open Asset Library

To access the library:

1. In the Toolbar, click the book icon.

    The Asset Library opens in a new window.

    ![The Asset Library open in Spatial Editor.](/images/spatial-editor-image-library.png)

## Find assets

To locate specific assets within the library, choose either **All** or other specific categories in the menu on the left.

**Note:** The Materials category is only available when accessed from the [Object tab](/documentation/spatial-sdk/spatial-editor-navigation-ui#object-tab)

## Import assets

To add an asset to your project:

1. Select the desired asset.
2. Click the download icon to import it.

## 3D primitives

3D primitives are available for prototyping. To find them:

1. Open the Asset Library.
2. Select **Primitives** from the menu on the left.

Alternatively, you can click on the primitives displayed in the [Toolbar](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-toolbar) to import them directly into your composition.

## Furniture assets

Furniture assets are available by default. To add them:

1. Open the Asset Library.
2. Select **Furniture** from the menu on the left.

## Manage materials

Materials from the Asset Library can be applied only within the [Object tab](/documentation/spatial-sdk/spatial-editor-navigation-ui#object-tab).

To use materials:

1. Double-click a 3D object in either the [Composition](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-composition-panel) or [Assets panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-assets-panel).
2. Reopen the Asset library from this tab.
3. The **Materials** category will be accessible in the left menu.

[Learn more about materials](/documentation/spatial-sdk/spatial-editor-materials-textures).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-bug-report.md
---
title: Report Spatial Editor bugs
description: Bug reports from our developer community help us improve features, fix problems and update documentation.
last_updated: 2024-09-10
---

Bug reports from our developer community help us improve features, fix problems, and update documentation. To report bugs or issues you find in Spatial Editor, click the bug report button at the top right of the application window:

![Bug report button.](/images/spatial-editor-report-bugs.png)

To make your bug report as useful as possible, please include:

* What were you trying to do?
* What happened instead?
* What are the exact steps to reproduce the issue?

Do not include any personal details about yourself or anyone else. Bug reports automatically contain information about your device to help us solve the issue.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-command-line-interface.md
---
title: Spatial Editor command line interface
description: Find out more about the Meta Spatial Editor command line interface (CLI). Export and create projects directly from the terminal.
last_updated: 2024-09-10
---

Spatial Editor includes a Command Line Interface (CLI), simplifying the process of exporting projects and integrating them with the Spatial SDK.

## Setup

To use the CLI, install Spatial Editor and open a terminal in the application's folder. Prefix your commands with the full path to the folder. For example, to export a project on MacOS, you would use:

```
/Applications/Meta Spatial Editor.app/ export -p /path/to/project.metaspatial -o /path/to/output/directory
```

## Export a project

The export command is exports a project from Spatial Editor. You can specify input and output paths, and the type of export desired, through these options:

- `-h` or `--help`: Displays a help message and exits.
- `-p` or `--project`: Sets the path to the project file you wish to export.
- `-o` or `--output`: Defines the path to the output file or directory for the exported project.

For example, to export an entire project located at `/path/to/project.metaspatial` to a specified directory, use:

```
export -p /path/to/project.metaspatial -o /path/to/output/directory
```

Include the application folder path at the beginning of your command. If integrating with a Spatial SDK app, export to the scenes directory.

## Export a composition or object

You can also export specific components of a project, such as a composition or an object, by using the export_options group:

- `-c` or `--composition`: Specifies the path to the .metaspatialcomposition file.
- `-b` or `--object`: Specifies the path to the .metaspatialobject file.

The output format depends on what you are exporting:

- .metaspatialobject files are exported as .gltf files.
- .metaspatialcomposition files are exported as .glxf files.

These examples export the specified composition or object to the output file specified by `-o`. The output file extension is determined by the input file type (.glxf for a composition, .gltf for an object).  To export a specific composition:

```
export -c /path/to/composition.metaspatialcomposition -o /path/to/output/file.glxf
```

To export a specific object:

```
export -b /path/to/object.metaspatialobject -o /path/to/output/file.gltf
```

`export --help` will display a help message that lists all of the available options for the export command.

Remember to include the path to the Spatial Editor application folder at the start of your command.

## Create a new project

The create command creates a new project in the specified directory:

*   `-p` or `--path`: Mandatory: Specifies the directory for the new project.
*   `-h` or `--help`: Prints a help message listing available options.

For example:

```
create -p /path/to/project
```

If you are creating a project inside your Spatial SDK file directory, you should choose the Scenes folder at `./app/src/main/scenes/`, which might already contain a default project.

**Note:** Always start your command with the path to the Spatial Editor application folder for proper execution.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-components.md
---
title: Components in Spatial Editor
description: Find out more about creating and using components (part of the Entity-Component-System design pattern) in your Meta Spatial Editor project.
last_updated: 2025-02-19
---

Spatial SDK apps leverage an [Entity-Component-System (ECS) design pattern](/documentation/spatial-sdk/spatial-sdk-ecs/). This design pattern enhances data organization on an entity through components and drives behavior with systems that process this data.

## Add components to an object

To add a component to an object:

1. Select the desired object in the **Composition** panel or the Viewport.

    **Note**: Adding components from the Object tab is not supported.

2. Navigate to the **Properties** panel and click the **+** button adjacent to Components.

3. A menu displaying available components will appear. Select the desired component to add it to your object, provided it doesn't already include that component.

It’s important to remember that adding components from the **Object** tab is not supported. Attributes such as map attributes, tuple attributes, and entity attributes are not supported either.

### Reload components
In the upper right corner of the **Component** menu, you can see a **Reload** button that allows you to instantly reload the changes you make in the [component XMLs](/documentation/spatial-sdk/spatial-sdk-component#creating-a-new-component). If you modify component [attributes](/documentation/spatial-sdk/spatial-sdk-attributes) in XML, clicking this button will refresh the list of available components. However, if you change the name of your component, you'll need to rebuild your app in Android Studio and then click the **Reload** button.

![](/images/spatial-editor-component-menu.png)

## Built-in components

Spatial Editor includes several predefined components tailored for frequent use cases, which you can add to your objects just like custom components. For built-in components to be available in the Spatial Editor, you need to open and build your project in Android Studio once.

| Component name | Description | Properties |
| --- | --- | --------- |
| Animated | Plays an animation for a glTF asset. Also configures different settings for animation. | pausedTime — Paused location/time (sec) within animation track <br/>playbackState — State of the animation (playing or paused) <br/>playbackType — The type of animation playback to be used <br/>startTime — World time at which animation started (ms since epoch) <br/>track — which animation track of the glTF to play |
| Audio | Plays audio “from” an entity | audioInternal — The Uri String of the audio file to be used <br/>volume — Volume of audio |
| AvatarAttachment | Defines the type of an Avatar the entity is meant to represent.   | type — Which part of the avatar the entity is meant to represent (i.e. “head”, “body”, “right_hand”, “left_controller”) |
| Box | Defines the dimensions of a box shape by the relative offset of two opposite corners. A box with max=Vector3(1,1,1) and min=Vector3(-1,-1,-1) will result in a 2 by 2 by 2 box | max — The relative offset of the top corner of the box from the center <br/>min — The relative offset of the bottom corner of the box from the center |
| Controller | Represents Controller Data and properties that can be used to facilitate input | buttonState — The current state of the buttons being pressed represented by integer bits <br/>changedButtons — Which buttons (represented by integer bits) have been changed (pressed or unpressed since the last frame) <br/>directTouchButtonState — The state of the direct touch buttons <br/>directTouchEnabled — Whether direct touch is enabled for this controller or not <br/>type — What type of controller it is. 0 for controller, 1 for hands, 2 for eye. |
| CreatorVisibility | Use this Component to hide an Entity from every user except for the creator of the Entity or hide the entity from only the creator. This *MUST* be used with dynamically created Entities. This Component is currently only designed for simple use like having an object or panel that only the creator can see. If you need more complex visibility logic, you will need to write your own Visibility Component and System. Feel free to use this one as a reference.  | state — Different states of CreatorVisibility, such as only visible to the creator, or only invisible to the creator |
| Dome | Defines the dimensions of a dome shape by a radius. | radius — The radius of the dome in meters |
| Grabbable | Grabbable is a component that allows an object to be grabbed by a controller. It requires the Mesh Component to be present.  | enabled — Defines whether the object can be grabbed or not. <br/>isGrabbed — Whether the object is currently grabbed or not <br/>maxHeight — the maximum height an object can be held when grabbed <br/>minHeight — the minimum height an object can be held when grabbed <br/>type — The type of behavior an object has when grabbed (faces user, pivots on y axis, etc.) |
| Hittable | Defines whether an object is hittable or not | hittable — The type of behavior the object can be hit using |
| Plane | Defines the dimensions of a horizontal plane | depth — The full length of the plane along the z axis <br/>width — The full length of the plane along the x axis |
| Quad | Dimensions for a Quad. | max — The offset of the top right? corner of the quad from the center of the quad <br/>min — The offset of the bottom left? corner of the quad from the center of the quad |
| RoundedBox | Defines the dimensions of a box shape with rounded corners by the relative offset of two opposite corners and a Vector3 of radii to modify the roundedness | max — The relative offset of the top corner of the box from the center <br/>min — The relative offset of the bottom corner of the box from the center <br/>radius — Vector3 representing the roundedness (follow up on exact modification) |
| Sphere | Defines the dimensions of a sphere by the radius | radius — The radius of the sphere in meters |
| SupportsLocomotion | When added to an entity with a mesh, allows for default locomotion on the mesh | N/A |
| TrackedBody | Maps joints found in BodyJoint to a Pose in world space. If a bone is not present in the map, it means that the tracking is not currently valid for that pose. Will be present locally if the XR_FB_body_tracking is able to be loaded. | jointPoses — This is an experimental attribute and not settable in Cosmo |
| Visible | Gives the ability to change mesh between being visible and invisible. | isVisible — The Mesh’s current state. |

## Create custom components

Spatial SDK allows for the creation of [custom components](/documentation/spatial-sdk/spatial-sdk-component/), acting as data containers within your application. Once integrated into a Spatial SDK project, these custom components become selectable and applicable to objects via the **Properties** panel.

While [XML](/documentation/spatial-sdk/spatial-sdk-component#creating-a-new-component) is the recommended way to define components, you can still use Kotlin. See the details [here](/documentation/spatial-sdk/spatial-sdk-editor#define-components-in-kotlin), but keep in mind that Kotlin usage is deprecated.

[Find out more about the Spatial SDK Gradle extension](/documentation/spatial-sdk/spatial-editor-using-with-sdk/)

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-compositions.md
---
title: Compositions
description: Learn more about creating compositions to use in your Meta Spatial SDK.
last_updated: 2024-09-10
---

In Spatial Editor, a composition is a spatial arrangement or scene that contains a hierarchy of [assets](/documentation/spatial-sdk/spatial-editor-import-manage-assets/), such as 3D models. You can create one or more compositions in a single project, and each composition is stored as an asset hierarchy in a [.glxf](/documentation/spatial-sdk/spatial-editor-file-compatibility#glxf) file.

Compositions are essential for constructing entire scenes for Spatial SDK applications or for creating reusable asset hierarchies. These hierarchies can be merged into single compositions at runtime, enhancing flexibility and reusability.

## Manage compositions

- **To create a new composition:** Click on **File** and select **New Composition**.
- **To open a composition:** double-click its .glxf file in the [**Project Assets** panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-assets-panel).
- **To edit a composition:** select its composition tab and make changes using the [**Composition** panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-composition-panel), [Viewport](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-viewport), and [**Properties** panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-properties-panel).
- **To add a new composition to your project:** click **File** and select **New Composition** in the top menu or tap the hotkey **C**.
- **To delete a composition**: go to the [**Project** tab](/documentation/spatial-sdk/spatial-editor-navigation-ui#project-tab) (the far left tab) and view your whole project hierarchy and assets. From there, you can see all your project's compositions in the hierarchy of the project in the left panel and delete them as needed.

## Group objects with empty nodes

When building a composition it's important to keep them organized and structured. This can help you navigate and manipulate your objects, and make it easier to understand the relationships between them.

To group objects under an empty node:

1. Click a node  you want to add to your group in the [**Composition** panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-composition-panel).
2. Right-click and select **Group**
3. Drag and drop each object you want to group under **Group**.
4. Right click the group and select **Rename** to title the group.

Alternatively, an empty node can be added to the composition by clicking the empty node icon at the top-right of the Composition panel.

When grouping and organizing 3D objects in your project:

- Use meaningful names for your groups and objects to make it easier to identify them later.
- Experiment with different grouping strategies to find what works best for your specific project.

## Work with multiple compositions

You can work with multiple compositions within a single project. These compositions could represent different scenes in your app, or be used to create prepackaged object hierarchies, akin to reusable blocks. You can change the behavior of the composition or objects within a composition depending on the state of the app.

## Instantiate assets into multiple compositions

Assets can be instantiated into multiple compositions. To do this, simply drag and drop the asset from the **Project Assets** panel into the desired composition. This allows you to reuse assets across different parts of your app, making it easier to maintain consistency and reduce duplication.

## Nest compositions

Compositions can be nested within other compositions. To nest a composition, drag and drop it from the **Project Assets** panel into another composition that’s open. This allows you to create complex object hierarchies and reuse entire compositions as building blocks for your app.

## Use your compositions with Spatial SDK

For instructions on exporting your project, loading compositions, and integrating content with Android, [refer to the guide on using Spatial Editor compositions](/documentation/spatial-sdk/spatial-editor-using-with-sdk/) in your Spatial SDK project.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-create-app-content.md
---
title: Build your first Spatial SDK app
description: This tutorial will give you hands-on practice building a spatial application using Meta Spatial Editor and Meta Spatial SDK. You will learn to understand the setup process, integrate and manipulate 3D models, utilize components effectively, and preview your work in a VR environment.
last_updated: 2025-03-17
---

This tutorial is an interactive walkthrough of the workflow you'll use when creating or converting an app with Meta's [Spatial Editor](/documentation/spatial-sdk/spatial-editor-overview) and Spatial SDK. If you're new to Android development and choose to do both the required and optional sections, you'll probably need at least an hour to complete this tutorial.

This tutorial will teach you how to:

- Set up a new Spatial SDK app, or add Spatial SDK to an existing 2D Android app.
- Import 3D assets.
- Manipulate 3D assets both programmatically and through Spatial Editor.
- Create and use custom components.
- Embed 2D content into a 3D VR environment as an interactable panel.
- Preview your app's VR environment.

## Before you begin

- Ensure your computer meets the [requirements to use Meta Quest Link](https://www.meta.com/en-gb/help/quest/articles/headsets-and-accessories/oculus-link/requirements-quest-link/).
- Install [Meta Spatial Editor](/horizon/downloads/spatial-sdk) for either Windows or Mac, which already includes the [CLI](/documentation/spatial-sdk/spatial-editor-command-line-interface) needed to export projects.
- Install the latest version of [Android Studio](https://developer.android.com/studio/) so you can develop and launch Android applications.
- Install [Spatial SDK's Android Studio Plugin](/documentation/spatial-sdk/spatial-sdk-android-studio-plugin/).
- Enable [developer mode](/documentation/native/android/mobile-device-setup/) on your headset.

## Choose a start option

To begin the tutorial, choose one of these options.
* If you want to build a Spatial SDK app from scratch, choose [Option A: Create a new Spatial SDK app](/documentation/spatial-sdk/create-new-spatial-sdk-app/).
* If you want to add Spatial SDK to an existing 2D Android app, choose [Option B: Add Spatial SDK to an existing 2D app](/documentation/spatial-sdk/add-spatial-sdk-to-app/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-download-setup.md
---
title: Download and setup Meta Spatial Editor
description: Download the latest version of Meta Spatial Editor, check system requirements and get started with your first project.
last_updated: 2024-09-10
---

Download the latest version of Spatial Editor on the [Spatial SDK downloads page](/downloads/spatial-sdk). By downloading, you agree to the Spatial Editor Terms.

**Note**: Spatial Editor is a spatial composition tool for Spatial SDK. It is not a standalone tool for creating Meta Horizon apps.

## System requirements (Mac)

- Minimum:
  - macOS 12.4 (Monterey)
  - Apple Silicon or Intel Core (2nd Gen)
  - 8GB RAM
  - GPU with Metal 2.2
- Recommended:
  - macOS 14 (Sonoma)
  - Apple Silicon
  - 16GB RAM
  - GPU with Metal 2.2

## System requirements (Windows)

- Minimum:
  - Windows 10
  - 4 cores with SSE4.2
  - 8GB RAM
  - 4 GB VRAM with OpenGL 4.6 (AMD GCN 4th gen, Nvidia GeForce 16 series, or Intel Rocket Lake).
- Recommended:
  - Windows 11
  - 8 cores
  - 16GB RAM
  - 8GB VRAM

## Open your first Spatial Editor project

If you're new to the Spatial SDK, follow these steps to open your first project in Spatial Editor:

1. Download the sample projects from the [Meta-Spatial-SDK-Samples](https://github.com/meta-quest/Meta-Spatial-SDK-Samples) GitHub repo.
2. Navigate to `Meta-Spatial-SDK-Samples/CustomComponentsSample/app/scenes`.
3. Open the `Main.metaspatial` file to see the project in Spatial Editor.

**Note**: Most of the sample projects come with a `Main.metaspatial` file stored inside of `app/scenes/`.

## Understand your project structure

The scenes directory in your Spatial SDK app should contain your entire Spatial Editor project. The following screenshot shows the `CustomComponentsSample` project opened in Android Studio:

![The scenes directory in a Spatial SDK project](/images/spatial-editor-export.png)

You can configure builds using the [Spatial SDK Gradle extension](/documentation/spatial-sdk/spatial-editor-using-with-sdk/).

For further assistance understanding Spatial Editor, visit the following resources:

- [Spatial Editor overview](/documentation/spatial-sdk/spatial-editor-overview/)
- [The user interface](/documentation/spatial-sdk/spatial-editor-navigation-ui/)
- [Compositions](/documentation/spatial-sdk/spatial-editor-compositions/)

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-file-compatibility.md
---
title: File formats and compatibility
description: Learn more about the files and formats you will be using to create with Meta Spatial Editor.
last_updated: 2024-03-25
---

## Overview

.glTF (and .glb), .obj, and .fbx are the only 3D formats that can be imported into a Spatial Editor project. To use 3D objects in other formats, convert them to .gltf or .glb using a tool like [Blender](https://docs.blender.org/manual/en/2.80/addons/io_scene_gltf2.html).

## glTF extensions

The glTF format includes [extensions](https://github.com/KhronosGroup/glTF/blob/main/extensions/README.md) that support additional features and effects in your 3D models. glTF extensions supported in Spatial Editor include:

- [unlit](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_materials_unlit/README.md)
- [texture_transform](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_texture_transform/README.md)
- [clearcoat](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_materials_clearcoat/README.md)
- [emissive_strength](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_materials_emissive_strength/README.md)
- [ior](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_materials_ior/README.md)
- [sheen](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_materials_sheen/README.md)
- [specular](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_materials_specular/README.md)
- [texture_webp](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Vendor/EXT_texture_webp/README.md)

[Find out more about materials and textures in Spatial Editor](/documentation/spatial-sdk/spatial-editor-materials-textures/).

## .glXF

[Compositions](/documentation/spatial-sdk/spatial-editor-compositions/) can be [exported](/documentation/spatial-sdk/spatial-editor-command-line-interface#export-a-composition-or-object) as glXF files, which are arrangements of glTF assets. [Find out more](https://github.com/KhronosGroup/glTF-External-Reference) about glXF files or [targeting  individual meshes in your Spatial SDK project](/documentation/spatial-sdk/spatial-editor-using-with-sdk/).

To export a composition as a glXF file, you can use the [Command Line Interface](/documentation/spatial-sdk/spatial-editor-command-line-interface/) (CLI) or select **File>Export glXF** in Spatial Editor. For more information on how to use the Spatial Editor CLI, [refer to the documentation](/documentation/spatial-sdk/spatial-editor-command-line-interface/).

## .metaspatial

The .metaspatial file extension is used for saving and loading projects in Spatial Editor.  A .metaspatial file brings together all the essential elements of your project, including 3D models, materials, textures, and other assets.

Ensure that the .metaspatial file and all related project files are placed in the Spatial Editor folder of your Spatial SDK project:

![The scenes folder of a Spatial SDK project.](/images/spatial-editor-export.png)

With the files saved in the correct directory, use the [Spatial SDK Gradle plugin](/documentation/spatial-sdk/spatial-editor-using-with-sdk/) to prepare your build. Alternatively, the [Spatial SDK template](/documentation/spatial-sdk/create-new-spatial-sdk-app) includes an empty Spatial Editor file for you to get started from.

Find out more about [adding a Spatial Editor project to a Spatial SDK app](/documentation/spatial-sdk/spatial-editor-using-with-sdk/).

## Supported texture formats

- **PNG**: This format is preferred for its lossless compression and ability to handle transparency. It's excellent for high-quality graphics where preserving detail is key.
- **JPEG**: Known for its efficient compression, JPEG is great for real-time graphics where both performance and reduced memory usage are crucial.

## Texture size guidelines

In the Spatial Editor, there is no strict limit on the size of textures you can use. However, for optimal performance, it's advisable to:

- Use textures whose sizes are powers of two (e.g., 64, 128, 256, 512, 1024).
- Ensure that textures are only as large as necessary for your application.

Key points to remember:

- Choose PNG for detailed, high-quality images with transparency.
- Opt for JPEG when you need to balance quality with performance and memory considerations.
- Stick to power-of-two texture sizes for better performance.

[Find out more about working with materials](/documentation/spatial-sdk/spatial-editor-materials-textures/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-import-manage-assets.md
---
title: Import and manage assets
description: Find out more about managing the objects and compositions that make up your Meta Spatial Editor project.
last_updated: 2024-09-10
---

In Spatial Editor, you primarily deal with two types of assets: [compositions](/documentation/spatial-sdk/spatial-editor-compositions/) and [objects](/documentation/spatial-sdk/spatial-editor-objects/).

[Objects](/documentation/spatial-sdk/spatial-editor-objects/) refer to 3D models and any associated data. The supported 3D formats for import into a Spatial Editor project are .glTF, .glb, .obj, and .fbx. To utilize 3D objects in other formats, convert them to .gltf or .glb using a conversion tool like Blender.

[Compositions](/documentation/spatial-sdk/spatial-editor-compositions/) represent an asset hierarchy. Upon export, they are converted to a .glxf file, which can be loaded and displayed in a Spatial SDK application. Your project can include multiple compositions, which consist of various objects and nodes.

## Import an object to your project

To import an object from your desktop:

1. Click the **+** button in the **Project Assets** panel.
2. Find and select the [.gltf or .glb](/documentation/spatial-sdk/spatial-editor-file-compatibility/) file that you want to import.

You can also import a .gltf or .glb file by dragging it from your computer's file browser directly into the [**Project Assets** panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-assets-panel).

For more detailed control over the import process, use the **Import Wizard** (File > Import Wizard). This allows you to select specific parts of the object to import, isolate particular meshes or materials, and exclude unwanted animations.

![The Spatial Editor import wizard.](/images/spatial-editor-import-wizard.png)

Assets can also be added to your project via the [Asset library](/documentation/spatial-sdk/spatial-editor-asset-library/), which is a curated library of assets provided by Spatial Editor.

## Add an asset to your composition

Once you import an asset, it will appear in the **Project Assets** panel. To add the asset to your composition:

1. Drag the object from the **Project Assets** panel directly into either the [Composition panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-composition-panel) or the [Viewport](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-viewport).

    The asset will then be visible in both the Composition panel and the Viewport.

## Animations

If your asset contains any animations, each track will be shown in the **Project Assets** panel when editing the object. When selecting an animation track, the animation playback controller will be shown in the [Properties panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-properties-panel). Here you can play, pause or reset the animation. The play bar also allows you to scrub through the animation:

![Playing and pausing an animation.](/images/spatial-editor-animation-fox.gif)

Animation tracks can be imported or excluded when using the import wizard. If importing without using the wizard, then all animation tracks will be included:

![The import wizard.](/images/spatial-editor-import-animation.png)

Animations in Spatial SDK apps can be controlled by adding the [**Animated** component](/documentation/spatial-sdk/spatial-sdk-animations#controlling-animations-in-a-meta-spatial-app) in the composition and selecting which track you want to play.

![Switching between tracks.](/images/spatial-editor-animation-component.png)

## Reuse assets

Your project can feature multiple instances of the same asset across different compositions. Editing an asset in one location, such as adjusting an object’s material properties in the Object tab, will automatically update all instances of that asset.

To track the usage of specific assets within your project, refer to the **Reference** list in the [Properties panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-properties-panel). Clicking a node in the Composition panel will display the asset it references:

![The references can be seen in the Properties panel.](/images/spatial-editor-transformation-properties.png)

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-keyboard-shortcuts.md
---
title: Keyboard shortcuts
description: Find out more about speeding up common Meta Spatial Editor workflows with keyboard shortcuts.
last_updated: 2024-09-10
---

To help speed up common workflows, Spatial Editor includes a range of keyboard shortcuts:

| Description | Shortcut |
|------|------|
| Select translation gizmo | T  |
| Select rotation gizmo | R  |
| Select scale gizmo | Y  |
| Select unified gizmo | U  |
| Pan viewport camera | CMD + left-click mouse drag (Mac) *OR* CTRL + left-click mouse drag (Windows) *OR* Two-finger swipe on trackpad |
| Dolly viewport camera | Option + left-click mouse drag (Mac) Alt + left-click mouse drag (Windows), or Pinch zoom on trackpad |
| Walk the viewport camera forward, left, backward, or right.  | W / A / S / D  or the arrow keys |
| Speed up the rate at which the viewport camera walks forward, left, backward, or right. | Shift + W / A / S / D or Shift + the arrow keys |
| Focus the viewport camera on the currently selected node.  | F |
| Open Meta Spatial Editor settings | CMD + , (Mac) *OR* CTRL + , (Windows)  |
| Create a new project  | CMD + N (Mac) *OR* CTRL + N (Windows)  |
| Open a project  | CMD + O (Mac) *OR* CTRL + O (Windows)  |
| Save current project | CMD + S (Mac) *OR* CTRL + S (Windows)  |
| Create a copy of the current project | CMD + Shift + S (Mac) *OR* CTRL + Shift + S (Windows)  |
| Export project | CMD + E (Mac) *OR* CTRL + E (Windows)  |
| Export object/composition | CMD + Shift + E (Mac) *OR* CTRL + Shift + E (Windows)  |
| Import  | CMD + I (Mac) *OR* CTRL + I (Windows)  |
| Import wizard | Shift+ CMD + I (Mac) *OR* Shift + CTRL + I (Windows)  |
| Duplicate (with node selected in Composition panel) | CMD + D (Mac) *OR* CTRL + D (Windows)  |
| Toggle left sidebar  | CMD + 1 (Mac) *OR* CTRL + 1 (Windows)  |
| Toggle right sidebar  | CMD + 2 (Mac) *OR* CTRL + 2 (Windows)  |
| Toggle bottom sidebar | CMD + 3 (Mac) *OR* CTRL + 3 (Windows)  |
| Toggle omnisearch | CMD + P (Mac) *OR* CTRL + P (Windows)  |
| Add to group (with node selected in Composition panel) | CMD + G (Mac) CTRL + G (Windows)  |
| Remove from group (with node selected in Composition panel) | CMD + Shift + G (Mac) CTRL + Shift + G (Windows)  |
| Create new object  | O |
| Create new composition | C  |
| Create new panel | P |

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-materials-textures.md
---
title: Materials and textures
description: Find out more about working with PBR materials in Meta Spatial Editor.
last_updated: 2024-09-10
---
Materials define the appearance of a 3D object’s surface. They consist of properties, like colors and textures, that work together to create the desired appearance.

## Material properties

The standard material component includes just one property: **Double Sided**. If it’s not selected, the faces using the material will only be visible on one side. From the other side, the faces will not be visible.

Other options, under **PBR Material Component**,  determine textures and how light interacts with the surface of your object. Here are the properties that make up a PBR material:

| Property | Type | Definition |
| :---- | :---- | :---- |
| *Base Color Factor* | Color | The main color of the material. If using a texture, leave this white (255,255,255) unless you want to tint the texture. |
| *Base Color Texture* | Texture | Applies varying color values across the geometry using texture coordinates. This will form the base of your material. Use it to add visible color and details.  |
| *Alpha Mode* | Text | This determines how the alpha value of the base color or texture is interpreted: In **Opaque** mode, the alpha value is ignored. In **Mask** mode, pixels are written off if the alpha value is > the alpha cutoff (see below). In **Blend** mode, the alpha value is used to blend with the color behind the object. Alpha value is the product of the base color texture alpha and the base color factor alpha.  |
| *Alpha Cutoff* | Percent | A parameter (between 0 and 100) that determines the cutoff point when **Alpha Mode**  is set to **Mask**. |
| *Metallic Factor* | Percent | This determines the extent to which the metallic channel of the roughness texture has an effect on the material. |
| *Roughness Factor* | Percent | This determines the extent to which the roughness channel of the roughness texture has an effect on the material. |
| *Roughness Texture*  | Texture | Maps different metalness and roughness values across the geometry using texture coordinates. The blue channel defines metalness, and the green channel defines roughness. Representing these details as a texture instead of geometry will increase the performance of your composition. The extent to which these textures are applied is adjusted using the metallic and roughness factor settings.  Spatial Editor packs ORM values into the RGB channels in that order. |
| *Normal Texture* | Texture | Used to create the appearance of real-world surface detail like bumps, grooves and rivets without adding extra geometry to your object. |
| *Occlusion Texture*  | Texture | Approximates soft shadows baked into the creased areas of a surface. The occlusion information is read from the red channel of the texture only.   |
| *Occlusion Strength* | Percent  | This determines the extent to which the occlusion texture has an effect on the material. |
| *Emissive Texture* | Texture | This texture provides emissive information indicating where the material should emit light. For example, power light indicators, LED displays or glowing eyes. |
| *Specular Factor* | Percent | The strength of the specular reflection. |
| *Specular Texture*  | Image | Specular describes the strength and color tint of the specular reflectivity on dielectric materials. This texture defines the strength of the specular reflection, stored in the alpha channel. This will be multiplied by the Factor. |
| *Specular Color Texture*  | Texture | A texture that defines the F0 (fresnel zero - a surface directly oriented toward the viewer) color of the specular reflection, stored in the RGB channels and encoded in sRGB. |
| *Specular Color*  | Color   | The F0 (fresnel zero - a surface directly oriented toward the viewer) color of the specular reflection. If using a texture, leave this white (255,255,255). |

## Change an object’s material

An object’s material can be changed or edited from the object editor:

1. Double-click the object in the **Composition** or **Project Assets** panel to open it in the object editor.
2. On the left, select a mesh from the **Object** panel (or select it directly from the Viewport).
3. On the right, click **+** next to the **Primitive**  heading to open the material picker.
4. Select a new material from the current object’s folder, or select a different object from the dropdown menu to use a material from elsewhere in your project.

![Changing an object's material.](/images/spatial-editor-materials.gif)

## Edit a material

To edit a material's properties:

1. With the object editor open, select a mesh from the **Object** panel. Make sure it uses the material you want to edit.
2. Hover over the material in the left-hand panel and click the three-dot menu (**⋯**) icon.
3. Select **Edit** from the dropdown menu.

Alternatively, selecting the material in the **Project Assets** panel will display material settings in the Properties panel on the right. To find out more about texture compatibility, visit this page on [file formats and compatibility](/documentation/spatial-sdk/spatial-editor-file-compatibility/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-navigation-ui.md
---
title: Navigate Spatial Editor
description: Explaining Meta Spatial Editor's user interface..
last_updated: 2024-09-10
---

## Overview

This page walks through Spatial Editor's user interface. Make sure you [download Spatial Editor](https://developers.meta.com/horizon/downloads/spatial-sdk) and [follow the setup instructions](/documentation/spatial-sdk/spatial-editor-download-setup).

## Welcome window

When you first open Spatial Editor, the welcome window gives you the option to create a new project or open an existing or recent project:

![The welcome window in Spatial Editor.](/images/spatial-editor-welcome.png)

## New project

When you create a new Spatial Editor project, it will contain one composition named **Composition 1**:

![Composition 1 in the Assets panel.](/images/spatial-editor-composition.png)

## The Viewport

The Viewport is centrally located to help you visualize, navigate, and preview your [composition](/documentation/spatial-sdk/spatial-editor-compositions). It displays a grid with units measuring one meter x one meter.

![The Viewport](/images/spatial-editor-viewport.gif)

You can navigate your composition using three modes:

- **Orbit** (default): Click and drag to rotate the Viewport around your selected object.
- **Pan**: Click and drag to move left, right, up, and down the Viewport. On Mac, you can also pan the Viewport with `Command+click-and-drag`. On Windows, use `Control+click-and-drag`.
- **Dolly**: Click and drag up or down to move back and forward. On Mac, you can also use the mouse scroll wheel, pinch the trackpad, or `Option+click-and-drag` in the Viewport. On Windows, use the mouse scroll wheel or `Alt+click-and-drag`.

![Spatial Editor stage](/images/spatial-editor-stage.png)

[Useful shortcuts for navigating the Viewport](/documentation/spatial-sdk/spatial-editor-keyboard-shortcuts).

## The Toolbar

Located at the top of the Spatial Editor window, the Toolbar facilitates the quick import of objects and creation of new compositions. It also allows you to add new panels or 3D primitives.

![The Toolbar](/images/spatial-editor-toolbar.png)

## The Composition panel

This panel is on the left side and becomes accessible when viewing a composition. It lets you search, select, and organize the nodes' hierarchy in your composition. To hide the panel, use the **View** menu, the left button on the toolbar, or the shortcut Command+1 (for Mac) or Ctrl+1 (for Windows).

![The Composition panel](/images/spatial-editor-composition-panel.png)

## The Properties panel

Situated on the right, this panel enables you to view and modify the properties of nodes selected from the Composition panel, such as translation, rotation, and scale:

![The Properties panel](/images/spatial-editor-properties.png)

Add Spatial SDK components to your objects using the **+** button next to [Components](/documentation/spatial-sdk/spatial-editor-components). If you select a material in the [Object tab](/documentation/spatial-sdk/spatial-editor-objects), this is also where you can adjust material properties. Hide this panel using the top right button on the Toolbar or the shortcut Command+2 (for Mac) or Ctrl+2 (for Windows).

## The Project Assets panel

The **Project Assets** panel, located at the bottom of the interface, is a powerful tool that allows you to manage and organize all the [assets]
(/documentation/spatial-sdk/spatial-editor-import-manage-assets) included in your project. It provides a comprehensive view of all the assets, not just those included in the open composition.

![The Assets panel](/images/spatial-editor-asset-panel.png)

An asset is a piece of content that can be reused across your project. There are two main types of assets in Spatial Editor: [Compositions](/documentation/spatial-sdk/spatial-editor-compositions) and [objects](/documentation/spatial-sdk/spatial-editor-objects). Compositions are containers for Spatial SDK content, made up of hierarchies of objects. Objects are 3D models and all associated data that you import with them.

The **Project Assets** panel offers functionality to manage your assets effectively. You can right-click on an asset to access a context menu with options such as Add to composition, **Update**, **Rename**, **Duplicate**, and more. Additionally, you can create folders and organize your assets into them, making it easier to find and access the assets you need.

## Project tab

The **Project** tab, located on the left-most side and labeled with the project's name, displays your project's complete hierarchy and an enlarged view of the **Project Assets** panel. Right-click on an asset to edit, rename, copy, delete, or duplicate it. You can also add new assets from this view.

![The Project tab](/images/spatial-editor-tabs.gif)

## Object tab

When you double-click an object in the **Composition** panel or the **Project Assets** panel, it opens in a new tab where you can edit the object. The object node hierarchy is listed in the **Object** panel on the top-left, and any assets referenced by the object are listed in the **Project Assets** panel on the bottom-left.

![The Project tab](/images/spatial-editor-object-editor.png)

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-objects.md
---
title: Objects in Spatial Editor
description: Find out more about working with and editing objects in Meta Spatial Editor.
last_updated: 2024-09-10
---

Once you have [imported an object](/documentation/spatial-sdk/spatial-editor-import-manage-assets/), the next step is to add it to your composition. Drag the file from the [**Project Assets** panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-project-assets-panel) directly into the [**Composition** panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-composition-panel) or [the Viewport](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-viewport). Alternatively, right click on the asset and select **Add to composition**.

Once you have added an object to a composition, it appears in both the Composition panel and the **Project Assets** panel:

- The entry in the **Project Assets** panel represents the asset itself.
- The node in the Composition panel represents an instance of that object. If the object is updated, all instances of it will reflect the update.

To monitor the usage of specific assets within your project, refer to the **Reference** list in the [**Properties** panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-properties-panel).

## Position and size objects  {#position-and-size-objects}

Manipulating your objects involves three fundamental concepts: Translation, Rotation, and Scale — collectively known as TRS values.

- **Translation**: Sets the object’s position in space, with X, Y, and Z values.
- **Rotation**: Sets the direction the object faces, in a circular movement around the object’s axes.
- **Scale**: Sets the size of the object relative to the composition.

You can use the Viewport gizmos to change these properties by direct manipulation, or select the object to edit its Translation, Rotation, and Scale in the [**Properties** panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-properties-panel):

![Changing the position of an object using the **Properties** panel.](/images/spatial-editor-transformation-properties-2.png)

See this [list of keyboard shortcuts](/documentation/spatial-sdk/spatial-editor-keyboard-shortcuts/) for tips on manipulating the viewport camera and objects.

## Translation gizmo

To activate the translation gizmo, select an object in your composition and click on the **Translation Gizmo** button at the top of the viewport or press the **T** key.

The translation gizmo will appear as arrows and dots. You can click and drag each arrow or dot to move the object within the 3D space:

- **Green Arrow**: Moves the object up and down (Y translation value).
- **Red Arrow**: Moves the object side to side (X translation value).
- **Blue Arrow**: Moves the object forward and backward (Z translation value).

The dots allow you to maintain one value constant while simultaneously altering the other two values:

- **Green Dot**: Maintains Y translation, altering X and Z values together.
- **Red Dot**: Maintains X translation, altering Y and Z values together.
- **Blue Dot**: Maintains Z translation, altering X and Y values together.
- **White Dot**: Allows unrestricted movement in any direction (changes X, Y, and Z values).

## Rotation gizmo

To activate the rotation gizmo, select an object  in your composition and click on the **Rotation Gizmo** button at the top of the viewport or press the **R** key. The rotation gizmo appears as semicircles around your object.

Click and drag any semicircle to adjust the rotation value of the object:

- **Green**: Rotates the object on the **Y** axis.
- **Red**: Rotates the object on the **X** axis.
- **Blue**: Rotates the object on the **Z** axis.

## Scale gizmo

To activate the scale gizmo, select an object and click on the **Scale Gizmo** button at the top of the viewport or press the **Y** key. The scale gizmo will appear as lines with small cubes at the ends, along with additional dots.

Click and drag the white cube in the center to uniformly scale the object, maintaining its shape while adjusting its size. Alternatively, you can click and drag any of the colored lines to change individual scale values:

- **Green**: Alters the **Y** scale value (stretches taller).
- **Red**: Alters the **X** scale value (stretches wider).
- **Blue**: Alters the **Z** scale value (stretches front to back).

Like the **Translation Gizmo**, the dots in the **Scale Gizmo** maintain one value constant while changing the other two values simultaneously.

## Fix X, Y, and Z value relations

Locking the X, Y, and Z value ratios maintains an object's dimensional proportions. This ensures consistent width, height, and depth when resizing or scaling. To fix the ratio, select fix to the left of scale.

![Fixing an object's scale.](/images/spatial-editor-fix-scale.gif)

## Edit an object

While Spatial Editor is not a 3D modeling tool, you can make some edits to an object. To edit an object, double-click it in the [**Project** tab](/documentation/spatial-sdk/spatial-editor-navigation-ui#project-tab), the [**Composition** panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-composition-panel) or the [**Project Assets** panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-project-assets-panel). This will open the object in a new tab, where you can update:

- The TRS values for any node, including the parent node.
- [Materials](/documentation/spatial-sdk/spatial-editor-materials-textures/), including textures, colors and other [PBR material values](/documentation/spatial-sdk/spatial-editor-materials-textures/).

## Use Spatial SDK components

Spatial Editor lets you add Spatial SDK [components](/documentation/spatial-sdk/spatial-editor-components/) to nodes in your composition via the [Properties panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-properties-panel). It also includes a range of component templates for common use cases.  By default, each new Spatial Editor project initiates with a components.json file. This file contains definitions for the built-in Spatial SDK components.

It's important to recognize that this file should not be manually altered. It is automatically updated by the Spatial SDK and Android Studio to reflect the latest available components, including any custom components.

## Add a component to an object

To add a component to an object:

1. Open the composition that includes the node where you want to add a component.
2. Select the desired node from either the Composition panel or the viewport.
3. In the Properties panel, click the **+** button next to Components.
4. A list of available components will display. Select the component you wish to add. It will automatically be added to the selected object, provided it doesn't already include that component.

**Note:** map attributes, tuple attributes and entity attributes are not supported. [Find out more about components in Spatial SDK](/documentation/spatial-sdk/spatial-editor-components/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-overview.md
---
title: Spatial Editor overview
description: Find out more about Meta Spatial Editor and get started designing scenes for MR applications.
last_updated: 2024-03-25
---

Spatial Editor ([download here](https://developers.meta.com/horizon/downloads/spatial-sdk)) is a spatial composition tool for Spatial SDK. Import, organize, and transform your assets into visual compositions and export them into [Spatial SDK](/documentation/spatial-sdk/spatial-sdk-overview/) projects to create immersive Meta Horizon OS experiences.

- Layout both 2D and 3D [objects](/documentation/spatial-sdk/spatial-editor-objects/) without writing any code, which speeds up iteration and creation.
- Assign [Spatial SDK components](/documentation/spatial-sdk/spatial-editor-components/) to objects directly within Spatial Editor instead of managing this logic in code.
- Use tooling that’s familiar to 3D artists and designers, facilitating faster and more efficient collaboration.

## Projects, assets, compositions and objects

A Spatial Editor project integrates with a Spatial SDK app containing all of the assets, compositions, and objects used in the app:

- An **asset** is a piece of content that can be reused across your project. This includes 3D models, materials, textures, and most importantly, compositions. [Find out more about managing assets in a Spatial Editor project](/documentation/spatial-sdk/spatial-editor-import-manage-assets/).
- **Compositions** act as containers for Spatial SDK content. They are made up of hierarchies of objects. [Find out more about compositions](/documentation/spatial-sdk/spatial-editor-compositions/).
- **Objects** are 3D models and all associated data that you import with them. Objects are then used to create your compositions. [Find out more about arranging objects in your compositions](/documentation/spatial-sdk/spatial-editor-objects/).

## Get started

Before you begin:

- [Download Spatial Editor](https://developers.meta.com/horizon/downloads/spatial-sdk/).
- Create a new project in Spatial Editor or use the [template Spatial SDK app](/documentation/spatial-sdk/create-new-spatial-sdk-app), which already includes an empty Spatial Editor project.
- [Integrate your project with a Spatial SDK app](/documentation/spatial-sdk/spatial-editor-using-with-sdk/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-panels.md
---
title: Panels in Spatial Editor
description: Find out more about placing and orienting panels in a Meta Spatial Editor composition and populating them with content using the Spatial SDK.
last_updated: 2024-09-10
---

## Overview

Spatial Editor allows you to place and orient multiple panels in a composition, as well as assign unique IDs needed for your Spatial SDK project.

## Understand panels in Meta Spark Spatial SDK

In the Spatial SDK, panels serve as containers for your 2D content. You can direct these panels to existing Android Activity code, which allows the panels to execute complete Android applications. The SDK is compatible with various 2D Android frameworks, giving you the flexibility to choose the framework that best suits your needs, or to continue using classic XML. For more detailed information on working with panels, you can [explore additional resources](/documentation/spatial-sdk/spatial-sdk-2dpanel/).

## Place and position panels

In Spatial Editor, panels are treated as nodes that can be placed into the composition and are manipulated using the same [translation, rotation, and scale gizmos](/documentation/spatial-sdk/spatial-editor-objects#position-and-size-objects).

To add a panel to your composition, select the **Add a 2D Panel** icon from the Toolbar:

![Adding a panel to a composition.](/images/spatial-editor-panel-placement.gif)

## Populate a panel using Spatial SDK

Each panel in Spatial SDK is identified by a unique ID. To assign or update an ID:

1. Select the desired panel within your composition.
2. Navigate to the [Properties panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-properties-panel).
3. Enter a unique string into the ID field.

Assigning a unique ID is crucial because it differentiates each panel within your project, enabling specific interactions and content displays. Find out more about [populating panels](/documentation/spatial-sdk/spatial-sdk-2dpanel/#bring-your-own-layout-framework).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-project-folder.md
---
title: Spatial Editor project folder structure
description: The Meta Spatial Editor project folder contains all of the assets and compositions that make up your Meta Spatial SDK app.
last_updated: 2024-09-10
---

The Spatial Editor project folder contains all of the [assets](/documentation/spatial-sdk/spatial-editor-import-manage-assets/) and [compositions](/documentation/spatial-sdk/spatial-editor-compositions/) in your Spatial SDK app. This folder may initially be empty if no assets or compositions have been included yet.

## Key components of the project folder

Inside the project folder, there are several folders and files:

- **Main.metaspatial**: This file opens the project in Spatial Editor.
- **Main.metaspatialobject**: This file stores all the objects related to the project.
- **Main.scene:** This file stores and manages individual scenes within a project.
- **Main.metaspatialcomposition:** This file contains all the compositions for the project. Composition files act as containers for the entire composition, which can contain multiple scenes. They hold all the necessary data to recreate the composition's state.

![The folders that make up a Spatial Editor project.](/images/spatial-editor-project-directory.png)

## Compositions

Compositions consist of:

- **Objects:** 3D objects with associated data, used to build compositions.
- **Panels:** 2D surfaces displaying traditional Android content.

A single project may include multiple compositions, each of which is exportable as a [glXF](/documentation/spatial-sdk/spatial-editor-file-compatibility#glxf) file. Enhance objects with [Spatial SDK components](/documentation/spatial-sdk/spatial-editor-components/) or code targeting their ID to introduce interactivity and functionality.

## Project tab

The Spatial Editor workspace is organized into tabs, with the Project tab displaying a hierarchical view of all project nodes. In this tab, you can manage assets by renaming, deleting, or adding new ones. When you open a composition or object, it appears in a new tab for further editing.

![Moving between tabs in Spatial Editor.](/images/spatial-editor-tabs.gif)

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-transforms-coordinates.md
---
title: Transforms and coordinates
description: Find out more about working with coordinates in Meta Spatial Editor, and orienting the user in the scene.
last_updated: 2024-09-10
---

## Overview

An object’s transform describes its placement in your scene. A transform is made up of three elements:

- The **translation** of an object in the scene. The coordinates displayed in the properties panel relate to the object’s local coordinates.
- The **scale** of the object compared to its original size (1, 1, 1).
- The **rotation** of the object compared to its original orientation (0, 0, 0).

The values shown for these properties in the Inspector are the local properties. If an object is parented under another object, it will inherit changes in scale, position or rotation from the parent object, but the local transform values will stay the same.

## Coordinates and your Spatial SDK app

The user's initial location within your composition is set using Spatial SDK's [`scene.setViewOrigin()` API](/reference/spatial-sdk/latest/root/com.meta.spatial.runtime/scene).

The glXF files with your compositions can be inflated at a specific transform offset. This means that coordinates between Spatial Editor and your Spatial SDK application may not be a 1:1 match unless the glXF is inflated at (0,0,0), which is the default.

## Empty nodes

In Spatial Editor, an empty node can be used to group other objects. Objects grouped under a null object are known as its children. The children take on the properties of the null object. For example, if you make a null object bigger, any children will get bigger too.

Empty nodes are added to your composition from the composition panel:

![Adding an empty node to a composition or object.](/images/spatial-editor-empty-node.gif)

Any object parented under the empty node will use that node’s local coordinate system. This means that the location of the empty node is used as the 0,0,0 origin point for child objects.

## Gizmo settings

You can change the gizmo UI to be relative to either local or world space.

- **Local** keeps the gizmo's orientation relative to the selected object.
- **Global** keeps the gizmo oriented with world space.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-editor-using-with-sdk.md
---
title: Using a Spatial Editor project with Spatial SDK
description: Learn more about using your Meta Spatial Editor compositions and objects in a Meta Spatial SDK app.
last_updated: 2025-02-19
---

This guide outlines the steps to integrate Spatial Editor projects with Spatial SDK apps. Once integrated, your Spatial Editor project will be located in the scenes directory of your Spatial SDK app:

![The scenes folder in a Spatial SDK project.](/images/spatial-editor-export.png)

## Setup the Spatial SDK Gradle plugin

The Spatial SDK Gradle plugin is used to process your Spatial Editor project and export it so it can be used by your app. Meta collects telemetry data from the Spatial SDK Gradle Plugin to help improve MPT Products. You can read the [Supplemental Meta Platforms Technologies Privacy Policy](https://www.meta.com/legal/privacy-policy/) to learn more.

To get started, ensure you have the following:

- Android Studio installed.
- A new Android Studio Spatial SDK project created, ideally using a [starter sample](https://github.com/meta-quest/Meta-Spatial-SDK-Samples) as a template.
- Spatial Editor installed, which includes the Spatial Editor CLI for export tasks.

Next, with your project open in Android Studio:

1. Open the project's **build.gradle.kts** file (not the Gradle file in the `app` folder).
2. At the top of the file within the `plugins` block, insert these lines to include the Meta Spatial Plugin and KSP (Kotlin Symbol Processing tool):

```kotlin
  id("com.meta.spatial.plugin") version "0.6.0" apply (true)
  id("com.google.devtools.ksp") version "1.9.25-1.0.20"
```

3. Finally, add this line to the dependencies section:

```kotlin
ksp("com.meta.spatial.plugin:com.meta.spatial.plugin.gradle.plugin:0.6.0")
```

If you are using a Spatial SDK template application, some steps might already be completed.

## Running  Gradle tasks

Find the tasks available with the plugin in the Gradle sidebar under the `spatial` directory. Open the Gradle sidebar by clicking on the Gradle icon in the right sidebar of Android Studio. Android Studio may not configure all Gradle tasks by default. To configure all Gradle tasks so you can see and run them, enable **Configure all Gradle tasks during Gradle Sync** in **File > Settings> Experiemental** under the **Gradle** header. All Gradle tasks can be found under `Tasks/spatial`.

![Gradle tasks in Android Studio.](/images/spatial-editor-gradle-tasks.png)

To execute any of the tasks, either double-click them in the Gradle sidebar or run `./gradlew _task name_`.

## Export Spatial Editor projects

To prepare your Spatial Editor project for use in your Spatial SDK project, modify the build.Gradle file as follows:

```kotlin
val projectDir = layout.projectDirectory
val sceneDirectory = projectDir.dir("scenes")
spatial {
 allowUsageDataCollection = true
 scenes {
   exportItems {
     item {
       projectPath.set(sceneDirectory.file("Main.metaspatial"))
       outputPath.set(projectDir.dir("src/main/assets/scenes"))
     }
   }
  }
}

```

- `CliPath.set(...)`: the CLI executable's location. If not set, the plugin will search predefined locations and may fail if the CLI is not found.
- `exportItems`: Defines a list of projects and asset directories to be exported.

Ensure you replace the placeholder with the correct path to the Spatial Editor executable on your system.

## Make custom components available in Spatial Editor

Spatial SDK projects use [components](/documentation/spatial-sdk/spatial-editor-components/) for data storage. There are two ways to make custom components available in the Spatial Editor UI.

### Define components in XML

Add a component [XML](/documentation/spatial-sdk/spatial-sdk-component#creating-a-new-component) file in `app/src/main/components`. The Spatial Editor will read the XML defined in the folder and display your custom components in UI. If you prefer to use another directory, refer to [Specify the custom components folder](/documentation/spatial-sdk/spatial-sdk-component#specify-the-custom-components-folder).

### Define components in Kotlin (deprecated)

In Spatial SDK version 0.5.5+, components are defined using XML. However, you may encounter older version that use Kotlin to define components. See the details [Connecting Spatial Editor](/documentation/spatial-sdk/spatial-sdk-editor#define-components-in-kotlin). In those versions, you can make the `generateComponents` task run automatically after your build by adding this to your app level `build.gradle.kts`.

```kotlin
afterEvaluate {
    tasks.named("assembleDebug") {
        finalizedBy("generateComponents")
    }
}
```

You can replace `assembleDebug` with whichever task you're using to build your app. This will make it so that the generateComponents task runs anytime you build your app.

## Load and change between compositions

The following sample demonstrates how to change between two compositions (Composition1 and Composition2) when a UI button is pressed (button0):

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    ...
    //load the first composition by name
    loadGLXF("Composition1")
 }

override fun registerPanels(): List<PanelRegistration> {
    return listOf(
        PanelRegistration(R.layout.ui_example) {
          config {
            themeResourceId = R.style.PanelAppThemeTransparent
            includeGlass = false
            width = 2.0f
            height = 1.5f
          }
          panel {
            val button0: Button? = rootView?.findViewById<Button>(R.id.button0)
		  //when the UI button0 is pressed,load Composition1
            button0?.setOnClickListener { loadGLXF("Composition1") }
            val button1: Button? = rootView?.findViewById<Button>(R.id.button1)
  //when the UI button1 is pressed,load Composition2
            button1?.setOnClickListener { loadGLXF("Composition2") }
          }
        })
  }

  private fun loadGLXF(compositionName: String): Job {

    gltfxEntity?.destroy() // destroy previous gltfx entity if it exists
    gltfxEntity = Entity.create()
    return activityScope.launch {
      glXFManager.inflateGLXF(
          Uri.parse("apk:///scenes/${compositionName}.glxf"),
          rootEntity = gltfxEntity!!,
          keyName = compositionName)
    }
  }
```

## Target specific objects in a composition with logic

The following example shows how to target a specific node of your composition (environment) with logic (adjusting the visibility):

```kotlin
     // wait for GLXF to load before accessing nodes inside it
    loadGLXF().invokeOnCompletion {
      val composition = glXFManager.getGLXFInfo("example_key_name")

      // get the environment entity from the composition
      val environmentEntity: Entity? = composition.getNodeByName("Environment").entity

      // set the environment to be invisible on start
      environmentEntity?.setComponent(Visible(false))
    }

 private fun loadGLXF(): Job {
    gltfxEntity = Entity.create()
    return activityScope.launch {
      glXFManager.inflateGLXF(
          Uri.parse("apk:///scenes/Composition.glxf"),
          rootEntity = gltfxEntity!!,
          keyName = "example_key_name")
    }
  }
```

## Populate a panel using Spatial SDK

When populating panels using Spatial SDK, you can differentiate them by setting a unique ID in the Properties panel of Spatial Editor. Here are several methods to layout and define panel content:

- Set `layoutResourceId` with the R layout resource Id, and define the layout with classic XML.
- Set  `activityClass` with the activity class name, and delegate the layout and logic to the Activity class.
- Set `panelIntent` with the customized Intent object, which can pass parameters as invoking another activity.
- Call `view callback` to generate the layout view in runtime.

For example, this script populates a small panel using Jetpack Compose:

```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.material.*
import androidx.compose.runtime.*
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.Modifier
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text

@Composable
fun MyPanel() {
    Column(modifier = Modifier.padding(16.dp)) {
        Text(text = "Panel Title", style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(8.dp))
        Text(text = "This is a panel with some content")
    }
}
```

For an in-depth look at populating panels with 2D content, see the [Spatial SDK panel documentation](/documentation/spatial-sdk/spatial-sdk-2dpanel/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-2dpanel-communication.md
---
title: 2D panel communication
description: Spatial SDK supports native mechanisms of communicating between the immersive environment and panels.
last_updated: 2024-11-07
---

## Overview

Spatial SDK uses Android for rendering panels. If you want to update your panel from another panel, you will have to use native Android view models, depending on your UI framework of choice. For example, if you are using Jetpack Compose, you can manage two separate panels as `Composable` functions that react to state changes.

For example:

```kotlin
class PanelViewModel : ViewModel() {
    private val _panelData = MutableLiveData<String>("0")
    val panelData: LiveData<String> = _panelData
    fun incrementData() {
        val currentValue = _panelData.value?.toInt() ?: 0
        _panelData.value = (currentValue + 1).toString()
    }
}

@Composable
fun PanelOne(viewModel: PanelViewModel) {
    val panelData by viewModel.panelData.observeAsState("0")
    Column {
        Text(text = "Panel One: $panelData")
        Button(onClick = onIncrement) {
            Text("Increment")
        }
    }
}

@Composable
fun PanelTwo(viewModel: PanelViewModel) {
    val panelData by viewModel.panelData.observeAsState("0")
    Text(text = "Panel Two: $panelData")
}
```

## 2D-to-3D data driven communication

This `ViewModel` driven approach works in more cases than just 2D-to-2D communication. For example a Spatial SDK [System](/documentation/spatial-sdk/spatial-sdk-writing-new-system) can be driven by a shared `ViewModel`.

The following system spawns a sphere whenever a button is clicked inside a Compose panel:

```kotlin
class AddSpheresSystem(panelViewModel: PanelViewModel) : SystemBase() {
  var numSpheres = panelViewModel.numberOfSpheres.value

  override fun execute() {
    if (numSpheres < panelViewModel.numberOfSpheres.value) {
      val numSpheresToAdd = panelViewModel.numberOfSpheres.value - numSpheres
      numSpheres = panelViewModel.numberOfSpheres.value
      for (x in 0..(numSpheresToAdd - 1)) {
        Entity.fromSphere(
                .3f,
                Transform(Pose(Vector3(x = x - 1.5f, y = 1f, z = 1f))),
                FlatColorMaterials.TAN,
                Grabbable(),
                FloatingDependentOrb(),
            )
            .registerEventListener<ButtonReleaseEventArgs>(ButtonReleaseEventArgs.EVENT_NAME) {
                _,
                eventArgs ->
              if (eventArgs.button == ControllerButton.RightTrigger) {
                panelViewModel.incrementData()
              }
            }
      }
    }
  }
}
```

## 3D-to-2D data driven communication

If you look closely at the code example above, you'll see that a click listener is added to the spheres that spawn.

```kotlin
.registerEventListener<ButtonReleaseEventArgs>(ButtonReleaseEventArgs.EVENT_NAME) {
    _, eventArgs ->
        if (eventArgs.button == ControllerButton.RightTrigger) {
            panelViewModel.incrementData()
        }
}
```

This click listener modifies the `viewModel`, which can be picked up in a panel rendering the `ViewModel`.

```kotlin
@Composable
fun PanelTwo(viewModel: PanelViewModel) {
    val panelData by viewModel.panelData.observeAsState("0")
    Text(text = "Panel Two: $panelData")
}
```

## 2D-to-3D event driven communication

If you prioritize code association over data encapsulation in your 2D app, consider adopting an event-driven model. This model allows you to invoke functions in your `VRActivity` directly from your 2D activity. The `SpatialActivityManager` provides four main functions to facilitate this integration.

```kotlin
inline fun <reified T : AppSystemActivity> getVrActivity(): T
fun getAppSystemActivity(): AppSystemActivity
inline fun <reified T : AppSystemActivity> executeOnVrActivity(
    crossinline runnable: (activity: T) -> Unit
)
fun executeOnAppSystemActivity(runnable: (activity: AppSystemActivity) -> Unit)
```

You can use this to call into Spatial SDK from anywhere inside of your 2D application. For example:

```kotlin
SpatialActivityManager.executeOnAppSystemActivity { _ ->
    for (x in 0..2) {
        Entity.fromSphere(
            .3f,
            Transform(Pose(Vector3(x = x - 1.5f, y = 1f, z = 1f))),
            FlatColorMaterials.TAN,
            Grabbable(),
            FloatingDependentOrb(),
        ).registerEventListener<ButtonReleaseEventArgs>(ButtonReleaseEventArgs.EVENT_NAME) {
            _, eventArgs ->
                if (eventArgs.button == ControllerButton.RightTrigger) {
                    PanelViewModel.clickCount.value++
                }
        }
    }
}
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-2dpanel-compose.md
---
title: Jetpack Compose in Spatial SDK
description: Meta Spatial SDK supports Jetpack Compose to build 2D panels in a 3D scene.
last_updated: 2024-12-17
---

## Overview

[Jetpack Compose](https://developer.android.com/compose) is a modern toolkit for building native Android UIs. It simplifies and accelerates UI development on Android with less code, powerful tools, and intuitive Kotlin APIs.

Spatial SDK supports Jetpack Compose and any other UI frameworks. You can use Jetpack Compose within Spatial SDK to build 2D panels.

There are two ways to create panels in a 3D scene with Jetpack Compose:

- Create Android Views directly with Jetpack Compose, which is lightweight and high-performance.
- Create an Android Activity with Jetpack Compose, which is simple and suitable for converting existing Android apps into a VR experiences for Meta Quest.

## Create Android Views directly with Jetpack Compose

Incorporating Jetpack Compose directly within an Android View offers numerous advantages. By eliminating the need to create additional activities, you conserve resources and enhance the overall performance of your application.

### Add ComposeFeature in the immersive activity

Spatial SDK includes `ComposeFeature`, which offers a lifecycle owner implementing the `LifecycleOwner`, `ViewModelStoreOwner`, and `SavedStateRegistryOwner` interfaces. This feature manages the lifecycle, view models, and saved state efficiently.

```kotlin
  // Add ComposeFeature in the immersive activity
  override fun registerFeatures(): List<SpatialFeature> {
    return listOf(VRFeature(this), ComposeFeature())
  }
```

### Register the panel with ComposeView and lifecycle

In `PanelRegistration`, you can use `view` to define the layout and components of the view. To use Jetpack Compose, you can create a `ComposeView` and set the composable content as `content()`, as demonstrated below.

```kotlin
  override fun registerPanels(): List<PanelRegistration> {
    return listOf(
        PanelRegistration(R.integer.panel_id) {
          config {...}
          view { ctx ->
            ComposeView(ctx).apply {
              setContent { content() }
              setViewCompositionStrategy(
                  ViewCompositionStrategy.DisposeOnViewTreeLifecycleDestroyed)
              attachLifecycleToRootView(this)
            }
          }
        })
  }
  ...
```

With `ComposeFeature` added, you can set the Jetpack composable function using a predefined `composePanel` in `PanelRegistration`.

```kotlin
  override fun registerPanels(): List<PanelRegistration> {
    return listOf(
        PanelRegistration(R.integer.composed_panel) {
          config {...}
          // Add compose function
          composePanel { setContent { composableFunction() } }
        })
  }
```

You can then spawn the panel with the `Entity.createPanelEntity` API:

```kotlin
...
    Entity.createPanelEntity(
        R.integer.panel_id,
        Transform(Pose(Vector3(3.2f, 1.0f, positionZ), Quaternion(0f, 160f, 0f))),
        Grabbable(),
    )
...
```

## Create Android Activity with Jetpack Compose

### Define the Android activity layout with Jetpack Compose

Like a normal Android activity, you need to create the composable function by adding the `@Composable` annotation to the function name.

```kotlin
@Composable
fun MessageCard(name: String) {
    Text(text = "Hello $name!")
}
```

Then, create the activity for the panel and add the composable function into the activity.

```kotlin
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.Text

class PanelActivity : ComponentActivity() {
  override fun onCreate(savedInstanceBundle: Bundle?) {
    super.onCreate(savedInstanceBundle)
    setContent { MessageCard("Meta Spatial SDK") }
  }
}
```

Make sure the activity is defined in your `AndroidManifest.xml` and contains the tag `android:allowEmbedded="true"`. This allows the activity to be embedded into a panel.

### Register and spawn the panel

After creating the activity with Jetpack Compose, you can register the panel by `PanelRegistration`:

```kotlin
  override fun registerPanels(): List<PanelRegistration> {
    return listOf(
        PanelRegistration(R.integer.panel_id) {
          activityClass = PanelActivity::class.java
          config {
            width = 2.0f
            height = 1.5f
          }
        })
  }
```

Then, spawn the panel with `Entity.createPanelEntity` API:

```kotlin
    Entity.createPanelEntity(
        R.integer.panel_id,
        Transform(Pose(Vector3(3.2f, 1.0f, positionZ), Quaternion(0f, 160f, 0f))),
        Grabbable(),
    )
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-2dpanel-drm.md
---
title: Protected Content and DRM
description: Meta Spatial SDK supports displaying protected content and DRM.
last_updated: 2025-04-22
---

## Overview

You often need to display protected or DRM content in your app. Meta Spatial SDK supports displaying protected content in a variety of ways.

## Secure Layers

Meta Spatial SDK supports restricting content from screen capture.

If you want to prevent all content from being screen captured and show a black screen instead, you can utilize `com.meta.spatial.SECURE_LAYERS` in your application's manifest.

```xml
<application>
...
    <meta-data
        android:name="com.meta.spatial.SECURE_LAYERS"
        android:value="true"
    />
```

Alternatively, you can selectively toggle it with `Scene.setSecureLayers(Boolean)`.

If using [Layers](https://developers.meta.com/horizon/documentation/spatial-sdk/spatial-sdk-2dpanel-layers), you can hide individual layers from screen recording with `LayerConfig(secure = true)` or `SceneLayer.setSecure(true)`.

## DRM Content

For integrating L1 or L3 DRM content, Spatial SDK has a variety of methods of displaying this content which need to be configured.

### Activity Based Panels

On Spatial SDK version `0.6.0+` and Meta Horizon OS v76+, you are able to display DRM content on [Activity-based panels](https://developers.meta.com/horizon/documentation/spatial-sdk/spatial-sdk-2dpanel-registration#determine-a-ui-to-render-to-the-panel). The code below is the minimal configuration needed to enable this.

```kotlin
PanelRegistration(...) {
    // need to use an Activity here
    activityClass = MyPanelActivity::class.java
    config {
        // must use Layers and also set secure to true
        layerConfig = LayerConfig(secure = true)
        // must set mips to 1 to opt into direct-to-compositor rendering
        mips = 1
        // must not utilize the SceneTexture
        forceSceneTexture = false
        ...
    }
}
```

### Direct to Surface Rendering

On Spatial SDK versions `0.5.4+` and earlier Meta Horizon OS versions, you can utilize rendering directly to a secure surface to display DRM content. This is a more advanced technique and requires creating your `PanelSceneObject`s manually. However, this approach is much more performant than setting up an entire view for the panel.

The code below shows how to display DRM content using Exoplayer with this approach.

```kotlin
// inside your AppSystemActivity
val myEntity = Entity.create(Transform())
// this PanelSceneObject just creates with an unused surface (no input or display forwarding)
val panelSceneObject =
    PanelSceneObject(
        scene,
        myEntity,
        PanelConfigOptions(
            width = myWidth,
            height = myHeight,
            // need to use layers with secure = true
            // this will ensure a secure surface is also created
            layerConfig = LayerConfig(secure = true),
            // need to set mips = 1
            mips = 1,
            // make sure this is not true
            enableTransparent = false,
    ))
val exoPlayer = ExoPlayer.Builder(this).build()
// Important! set exoplayer to play on this protected surface
exoPlayer.setVideoSurface(panelSceneObject.getSurface())
```

### Hybrid Apps

For non-immersive apps running in Quest Home (such as hybrid apps), see [general Android DRM support](https://developers.meta.com/horizon/resources/2d-features#drm-support).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-2dpanel-layers.md
---
title: Layers and UI quality
description: Meta Spatial SDK supports using layers in 2D panels for higher visual fidelity.
last_updated: 2024-11-14
---

## Overview

By default, Spatial SDK optimizes panels to work well for most use cases. However, if you want to achieve a specific effect, you may have to do some deeper configuring.

## Layers in 2D panels

Spatial SDK has a layers feature that lets you get the best visual fidelity out of your panels. Layers provide a superior look but come with many tradeoffs. Below is a comparison of a panel with and without layers. The effect is much more noticeable when viewed from within your headset.

### Example of a panel not using layers

![Screenshot of a panel that is blurry and not using layers](/images/fa_aether_no_layer.png)

### Example of a panel using layers

![Screenshot of a panel that is not blurry and using layers](/images/fa_aether_layer.png)

More details can be found [here](/documentation/native/android/os-compositor-layers).

## Layers example

This example shows how to add layers to your panels and should work in most general use cases.

```kotlin
...
  override fun registerPanels(): List<PanelRegistration> {
    return listOf(
        PanelRegistration(R.layout.ui_example) {
          ...
          config {
            ...
            layerConfig = LayerConfig()
            enableTransparent = true
          }
          ...
        })
  }
```

You can also specify the layer configuration directly:

```kotlin
import com.meta.spatial.runtime.AlphaMode
import com.meta.spatial.runtime.LayerConfig
import com.meta.spatial.runtime.SceneMaterial


  override fun registerPanels(): List<PanelRegistration> {
    return listOf(
        PanelRegistration(R.layout.ui_example) {
          ...
          config {
            ...
            // tells the panel to use layers
            layerConfig = LayerConfig()
            // sets up the hole punching
            alphaMode = AlphaMode.HOLE_PUNCH
            panelShader = SceneMaterial.HOLE_PUNCH_PANEL_SHADER
            forceSceneTexture = true
            ...
          }
          ...
        })
  }
```

If you don’t want to use layers, simply remove `layerConfig` from your configuration, along with the `panelShader` and `alphaMode` changes.

## Technical explanation

Use [OpenXR Layers](https://registry.khronos.org/OpenXR/specs/1.0/html/xrspec.html#composition-layer-types) to get the best quality out of your panels. These layers allow you to submit your panel directly to the OpenXR compositor, which minimizes the amount of sampling required and produces the highest quality images possible.

The technical details can be found [here](https://developers.meta.com/horizon/documentation/native/android/os-compositor-layers),

Using OpenXR layers comes at a cost. For example, these layers won't be composited into your panel in the scene. Instead, OpenXR will either render the layers below or above your scene. If you try to render a layer without extra configuration, it will render above your screen. This is fine in some cases, but if you try to bring something like a controller in front of the panel, the panel will render over the controller instead.

You can use the hole punching technique to resolve this issue. Hole punching means rendering the layers first and then rendering the scene on top of them. This technique covers up your layers, but you can punch holes in the scene to clear out the pixels and reveal the layers underneath.

Here is an illustration of how hole punching works:

![Example diagram of how hole punching works](/images/fa_aether_holepunch.jpg)

In Spatial SDK, layers render above the scene unless you enable hole punching by calling `scene.enableHolePunching(true)`. This call causes Spatial SDK to render the layers before the scene. Spatial SDK enables hole punching by default. To disable it, you have to call `scene.enableHolePunching(false)`.

If you only enable hole punching and use the layers config, you will no longer be able to see your panels, because you haven’t punched holes in the scene yet. To punch the required holes, you can use `panelShader = SceneMaterial.HOLE_PUNCH_PANEL_SHADER` and `alphaMode = AlphaMode.HOLE_PUNCH`. These two calls do the following:

- Tells the panel mesh in the scene to only write to the depth of the mesh.
- Clears all color and alpha values, which causes the scene to show through to the layers beneath.

You can get creative with layers and blending modes (set in the layer config) to achieve interesting effects like masking and additive blending.

## Restrictions

- Transparency: Transparencies are challenging because you need to have your panel punch holes in the places where your panel has transparency. This hole punching is hard to do arbitrarily. You can sometimes use `panelShader = SceneMaterial.HOLE_PUNCH_PANEL_SHADER` to get around the difficulty of ad hoc hole-punching.
- Overlapping or intersecting layers: Spatial SDK writes layers one-by-one and does not write depth. This can sometimes make overlapping panels an issue.
- Shader capabilities: You can attach an effect process to our panel, but the compositor handles the final image rather than our shaders, so we cannot edit the panel with a custom shader after the fact.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-2dpanel-registration.md
---
title: Register 2D panels
description: Meta Spatial SDK supports registering a panel to the scene with PanelRegistration.
last_updated: 2024-10-21
---

## Overview

To use 2D panels, you need to register and [spawn](/documentation/spatial-sdk/spatial-sdk-2dpanel-spawn) them in your 3D scene. This page covers the process of registration.

## Registering your panel with `PanelRegistration`

You can think of panel registration as creating a blueprint for your panel. However, it does not actually add the panel to the scene. To spawn a panel into your scene, you must add an Entity with a Panel component that references this blueprint. This is covered in [Spawn and remove 2D panels](/documentation/spatial-sdk/spatial-sdk-2dpanel-spawn/).

To register a panel, you create a `PanelRegistration` object and configure it for your specific panel. Here is an example `PanelRegistration` configuration:

```kotlin
import com.meta.spatial.toolkit.PanelRegistration
...
  // In your immersive activity, override registerPanels() and return a list of PanelRegistration objects
  override fun registerPanels(): List<PanelRegistration> {
    return listOf(
        PanelRegistration(R.layout.panel_control) {
          // layoutResourceId defaults to the id passed into the PanelRegistration() constructor
          // layoutResourceId = R.layout.panel_control
          config {
            width = 2.0f
            height = 1.5f
          }
          panel {
            rootView
                ?.findViewById<Button>(R.id.create_button)
                ?.setOnClickListener({ createPanel(R.integer.custom_panel_id) })
            rootView
                ?.findViewById<Button>(R.id.destroy_button)
                ?.setOnClickListener({ Entity(R.integer.custom_panel_id).destroy() })
          }
        },
        PanelRegistration(R.integer.custom_panel_id) {
          activityClass = MyPanel::class.java
        })
  }
...
```

You can also register a panel dynamically in your immersive activity by calling the `registerPanel()` API:

```kotlin
      registerPanel(
          PanelRegistration(somePanelRegistrationId) {
            config {
              includeGlass = true
              enableLayer = true
              enableTransparent = true
            }
            view { ctx ->
              val view = LinearLayout(ctx)
              val button =
                  Button(ctx).apply {
                    text = "Turning Blue"
                    setBackgroundColor(Color.BLUE)
                    setOnClickListener { v ->
                      val c = v.background as ColorDrawable
                      view.background = c
                    }
                  }
              view.apply { addView(button) }
            }
          })
```

Panel registration involves a few critical elements:

- Defining an ID for the panel.
- Determining a UI to render to the panel.
- Configuring the panel.
- Hooking-up behavior to layout within the panel.

### Define an ID for the panel

A `registrationId` must be passed in the constructor for `PanelRegistration`. This ID links your `PanelRegistration` definition to the Panel Entity in your scene (your Panel Entity must also supply the exact same ID).

While the ID can be any integer, using a resource ID is recommended.
- `R.layout.{id here}` if you are using layout XML for the UI in the panel.
- `R.id.{id here}` for anything else.

You can create multiple Entities in your scene with the same UI by creating multiple Panel Entities that point to the same `PanelRegistration` ID.

### Determine a UI to render to the panel

You can choose your own UI framework to create the UI that appears in your panel. The panel UI can be defined in one of four ways:

1. **Layout XML**: Set `layoutResourceId` with an R.layout resource ID and build your UI with layout XML.
2. **Activity**: Set `activityClass` with the activity class name and delegate the layout and logic to the Activity class.
3. **Intent**: Set `panelIntent` with an Intent, allowing you to pass parameters to an Activity that will be started up in the panel.
4. **Runtime**: Call the `view{}` callback to generate your layout view at runtime, as demonstrated in the code block above.

Running many activities simultaneously reduces performance. Be careful not to create too many Activity-based panels.

### Configure the panel

The `config` argument allows you to customize your panel by passing in a `PanelConfigOptions` object. You can change several things, such as height and width. You can even create a glass encasing around the panel.

This example shows how you would set your configuration options to accomplish this:

```kotlin
  override fun registerPanels(): List<PanelRegistration> {
    return listOf(
        PanelRegistration(R.layout.panel_control) {
          ...
          config {
            width = 2.0f
            height = 1.5f
            includeGlass = true
          }
          ...
        })
  }
```

For more information on advanced configurations, see [2D panel config and resolution](/documentation/spatial-sdk/spatial-sdk-2dpanel-resolution/) and [2D UI quality](/documentation/spatial-sdk/spatial-sdk-2dpanel-layers/).

### Hook-up behavior to layout within the panel

When you create a Spatial SDK panel, a `PanelSceneObject` object is added to your scene. The `panel` callback is how you customize your `PanelSceneObject`.

Here is an example of a panel defined by layout XML UI that responds to button presses:

```kotlin
  override fun registerPanels(): List<PanelRegistration> {
    return listOf(
        PanelRegistration(R.layout.ui_example) {
          ...
          panel {
            // Set background of this panel
            val click =
                View.OnClickListener { v ->
                  val c = v.background as ColorDrawable
                  val chosen = rootView?.findViewById<LinearLayout>(R.id.ui_example_layout)
                  chosen?.background = c
                }
            rootView?.findViewById<Button>(R.id.red)?.setOnClickListener(click)
            rootView?.findViewById<Button>(R.id.spawn_panel)?.setOnClickListener(createPanel())
          }
          ...
        })
  }
```

## (Advanced) Register your panel with `PanelCreator`

If `PanelRegistration` is not flexible enough for you, you can register your panel with `PanelCreator`, which takes a `registrationId` and a `PanelSceneObject` creator function.
In the creator function, you can define any logic to generate the `PanelSceneObject` which will represent the panel in the scene.

```kotlin
import com.meta.spatial.toolkit.PanelCreator
import com.meta.spatial.toolkit.PanelRegistration

...
  override fun registerPanels(): List<PanelRegistration> {
    return listOf(
        ...
        PanelCreator(R.layout.activity_main) { ent -> createMainActivity(ent) },
        ...)
  }
  ...
  private fun createMainActivity(ent: Entity): PanelSceneObject {
    val config = PanelConfigOptions(height = 2f, includeGlass = false)
    return PanelSceneObject(scene, this, Intent(this, MyPanelActivity::class.java), ent, config)
  }
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-2dpanel-resolution.md
---
title: 2D Panel Config and Resolution
description: Control the resolution and size of 2D panels
last_updated: 2024-10-21
---

## Overview

In `PanelRegistration`, you can define the panel's config options, which determine the panel's size and layout. You may want to adjust the panel’s layout to make the panel look sharper.

Consider a real-world screen, such as a TV or phone. These screens have specific resolutions, such as 4k for TVs or 1080 x 2280 for phones. The clarity of the image on these screens depends on their distance from you. Close-up, the screens appear clearer, while those further away might seem blurry. Additionally, the screen's field of view (FOV) influences whether you can see the display clearly.

In a 3D scene, the clarity of the panel depends on its resolution and its FOV relative to the eye buffer of the Quest device. You can adjust this clarity by modifying the panel's size and position in relation to the VR/MR viewpoint.

For reference, Quest 3's eye buffer screen resolution is 2064 x 2208, and the FOV is 110° x 96° per eye.

![FOV](/images/fa_aether_panel_fov.png)

## 2D panel resolution

In the panel configuration, you can define:

- `layoutWidthInDp`/`layoutHeightInDp`: the panel layout's width and height in [density-independent pixels](https://developer.android.com/training/multiscreen/screendensities) to maintain consistent layout content across various screen densities. This approach is similar to common Android layouts, ensuring that adjustments in the panel's pixels do not affect the layout's appearance.
- `layoutDpi`: the dots per inch (DPI) of a panel, similar to an Android screen's DPI, determines its width and height in DP. Increasing the DPI enhances the panel's density, thereby improving its resolution. By default, panels have a DPI of 256, a value empirically set based on the eye buffer of Quest 2 and adjusted to accommodate Quest 3's size.
- `layoutWidthInPx`/`layoutHeightInPx`: the panel layout's width and height in pixels. Panels will use them to create Android `VirtualDisplay` with `DPI`. If not defined specifically, they will be derived from `layoutWidthInDp/layoutHeightInDp` and `DPI`.
- `width`/`height`: the panel's scene object size, with width and height in meters. In mixed reality/VR, the width/height will be the physical size of the panel.
- `fractionOfScreen`: determines the panel's width as a percentage of the rendering screen, specifically for Quest devices' eye buffer. If `layoutWidth/HeightInDp` or `layoutWidth/HeightInPx` are undefined, the panel defaults to using `fractionOfScreen`. For instance, setting `fractionOfScreen = 0.5` implies the panel occupies half the screen's width. The height is then derived from the width based on the height-to-width ratio. In a Quest 3 device, with `fractionOfScreen = 0.5`, the calculations would be layoutWidthInPx = 2064 * 0.5 and layoutHeightInPx = layoutWidthInPx * height/width ratio

## Building and rendering panels in 3D

To understand these configurations, it's important to know how the panels are built and rendered in a 3D scene.

Here's the high level process:

1. Build the panel content with an Android `VirtualDisplay`, and render the display as scene texture.
  - Create the Android screen/display with `layoutHeightInPx`/`Width` and DPI.
  - DPI defines the clarity of the panel screen. Together with the height/width in pixels, they will determine the size of the panel of the Android display.
  - With the Android display/screen, you'll get the scene texture of the panel.
2. Build the Spatial SDK 3D mesh (surface or cylinder) and attach the panel’s texture to the surface of 3D object.
  - For the panel, you will build the 3D object/mesh. For example, for a quad panel, you will create a box with height/width and nearly zero thickness.
  - The height and width are from the attributes of panel config, and are measured in meters in the 3D scene.
  - Adjusting the height/width will only scale the panel scene texture (not resize it), which can make it blurry if scaling height/width too large.
3. Rendering the panel scene object to the eye buffer, the screen of the Quest.
  - With the panel object/mesh in the 3D scene, you can render it to the eye buffer, like any other 3D objects.
  - As you move closer or farther from the panel, the FOV of the panel will update.
  - You can also create a system to scale or pivot the panel, like the [custom components sample app](https://github.com/meta-quest/Meta-Spatial-SDK-Samples/tree/main/CustomComponentsSample), keeping the panel facing you or its FOV the same.

## Resolution calculation

### Calculating an Android virtual device's size and resolution

You might want to use [Android virtual devices](https://developer.android.com/studio/run/managing-avds) to build and test your 2D panels layout.

Here's an example of how to calculate the 2D panel's size and resolution for Android virtual devices.

- Assume you want to set the panel's FOV to `Fraction of Screen = 0.5`.
- Calculate the width in pixels:

```
WidthPx = Eyebuffer Width * Fraction of Screen
        = 2064 * 0.5
        = 1032
```

You can also adjust this manually.

- Calculate the height in pixels:

```
HeightPx = Eyebuffer Height * Fraction of Screen * (height / width)
         = 2208 * 0.5 * (3 / 4)
         = 828
```

You can also adjust this manually.

- Determine the default DPI:

```
DPI = 256 * Eyebuffer Width / 1832
    = 256 * 2064 / 1832
    = 288.419
```

You can also adjust this manually.

- Compute the width in DP:

```
Width DP = (WidthPx / DPI) * 160
         = (1032 / 288.419) * 160
         = 572.51
```

- Compute the height in DP:

```
Height DP = (HeightPx / DPI) * 160
          = (828 / 288.419) * 160
          = 459.34
```

- Calculate the diagonal in pixels:

```
Diagonal in Px = Sqrt(WidthPx^2 + HeightPx^2)
               = Sqrt(1032^2 + 828^2)
               = 1323
```

- Finally, calculate the diagonal in inches:

```
Diagonal in Inches = Diagonal in Px / DPI
                   = 1323 / 288.419
                   = 4.6
```

With all these calculations, you can set Android virtual device's screen size as 4.6 inches, and the resolution as 1032x828px.

![Calculation of Android virtual device's size and resolution](/images/fa_aether_panel_design.png)

### Calculating size and position for 2D panels in 3D scene

- Assume you want to set your panel's FOVE to `Fraction of Screen = 0.5`.
- For rendering on Quest 3, the panel should appear in the eye buffer as `1032x1104px`, calculated from `(2064/2)x(2208/2)px`.
- Define `layoutWidthInDp`, `layoutHeightInDp`, and `layoutDpi` to maintain a clear and stable layout. Use these to compute the panel texture's resolution:
  - `layoutWidthInPx` = layoutWidthInDp * layoutDpi / 160
  - `layoutHeightInPx` = layoutHeightInDp * layoutDpi / 160
  - Avoid setting `layoutWidthInPx`/`layoutHeightInPx` larger than 2064x2208px due to performance limitations.
- To ensure the `layoutWidthInPx` and `layoutHeightInPx` are rendered correctly in the eye buffer as 1032x1104px, adjust the panel's size and distance proportionally.
  - For example, for a width = 1.0 meter, set the viewpoint distance as 1032px / `layoutWidthInPx` * width.

![An example of the resolution calculation](/images/fa_aether_panel_resize.png)

## 2D Panel sizing and positioning

As mentioned before, you can set the panel's initial size in `PanelRegistration`:

```kotlin
...
  override fun registerPanels(): List<PanelRegistration> {
    return listOf(
        PanelRegistration(R.id.panel_id) {
          ...
          config {
            width = 2.0f   // In meters of VR/MR world
            height = 1.5f  // In meters of VR/MR world
          }
          ...
        })
  }
...
```

You can make the panel sharper and better-looking by sizing and positioning it accordingly. You can also the size with `Scale` components after creating the panel:

```kotlin
  panelEntity.setComponent(Scale(Vector3(scaledSize)))
```

For positioning, you can set and update the `Transform` component:

```kotlin
  panelEntity.setComponent(Transform(Pose(Vector3(x, y, z), Quaternion(x, y, z))))
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-2dpanel-spawn.md
---
title: Spawn and Remove 2D Panels
description: Meta Spatial SDK can spawn and remove 2D panels in a 3D scene.
last_updated: 2024-10-21
---

## Overview

To use 2D panels, you need to [register](/documentation/spatial-sdk/spatial-sdk-2dpanel-registration/) and spawn them in your 3D scene. This page covers the process of spawning a panel at runtime and using Spatial Editor.

## Spawn a panel to the scene

To generate a panel and render it in a Spatial SDK scene, you need to create an entity with a panel component attached to it. In the panel component, you need to pass the panel's `registrationId`. Behind the scenes, a [system](/documentation/spatial-sdk/spatial-sdk-ecs/) locates the panel registration using the `registrationId`, and spawns the panel automatically.

### Spawn your panel at runtime

The `Entity` class has an API called `createPanelEntity`, which takes a panel's `registrationId`, a `Transform` component, and other components, like `Grabbable()`.

Here is an example:

```kotlin
...
    Entity.createPanelEntity(
        R.integer.custom_panel_id,
        Transform(Pose(Vector3(3.2f, 1.0f, 1.0f), Quaternion(0f, 160f, 0f))),
        Grabbable(),
    )
...
```

### Spawn your panel using Spatial Editor

As described in [Panels in Spatial Editor](/documentation/spatial-sdk/spatial-editor-panels), you can add a panel to a Spatial Editor composition. The ID of the panel should be the `registrationId` that you defined in the `registerPanels` function.

![Spawn your panel by Spatial Editor](/images/fa_aether_cosmo_panel.png)

After saving the composition, the panel will be generated automatically.

For more information on Spatial Editor, see [Using a Spatial Editor project with Spatial SDK](/documentation/spatial-sdk/spatial-editor-using-with-sdk/).

## Removing a panel

To remove a panel, delete the associated entity.

```kotlin
myPanelEntity.destroy()
```

Spatial SDK systems will clean up your destroyed panel entity, including the panel component in it.

### Safely destroying activity-based panels

The activity associated with a panel cannot be terminated using the `finish()` method, as this may lead to application crashes. Calling the `finish()` method on an Activity can result in a crash due to the improper updating of the panel's resources, including the 3D mesh, layer, texture, and Android surface.

To properly destroy activity-based panels, use `panelEntity.destroy()`, as mentioned above.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-2dpanel.md
---
title: 2D panels in Spatial SDK
description: Meta Spatial SDK supports using 2D panels as 3D objects in a 3D scene.
last_updated: 2024-10-21
---

## Overview

Spatial SDK lets you use any Android UI framework to create 2D UIs, then create a panel for them in your 3D scene. Spatial SDK handles rendering and input handling for you, allowing you to focus on creating UIs.

Here is an example of panels in the video player sample app:

![2D panels in Spatial SDK](/images/fa_aether_video_panel.jpg)

## Why use 2D panels?

Integrating 2D panels into 3D scenes provides several benefits:

- **Present information clearly**: 2D panels excel at displaying text, images, and UI components with clarity and precision. This can be challenging with purely 3D elements.
- **Familiar user interface**: Panels offer a familiar interface, making navigation and interaction more intuitive in a 3D space.
- **Performance**: 2D elements are generally less resource-intensive than 3D objects. This helps maintain better performance in your applications.

## Integrate 2D panels as 3D objects

Follow these guides to add 2D panels into your scene:

1. [Register the panel definition](/documentation/spatial-sdk/spatial-sdk-2dpanel-registration/).
2. [Spawn the panel in the 3D scene](/documentation/spatial-sdk/spatial-sdk-2dpanel-spawn/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-3dobjects.md
---
title: 3D objects
description: Meta Spatial SDK has a model for loading and managing your 3D assets.
last_updated: 2024-11-11
---

## Overview

This document shows how to maximize Spatial SDK's model loading to load and manage 3D assets. Spatial SDK simplifies the process of loading and handling your 3D assets. For example, you can load your models by using `Mesh(Uri.parse("myMesh.glb"))`.

## Coordinate space

Spatial SDK uses a left-handed coordinate system, where X+ is to the right, Y+ is upward, and Z+ is forward. Any loaded glTF models will be converted to match this coordinate space. All units are in meters unless otherwise specified.

## The `Mesh` component

The primary way to load a 3D asset is via a `Mesh` component.

```
class Mesh(
    var mesh: Uri = Uri.parse("about:blank"),
    var hittable: MeshCollision = MeshCollision.LineTest,
    var defaultShaderOverride: String = "",
    var defaultSceneOverride: Int = -1,
)
```

Here is a closer look at each attribute.

- `mesh`: A [`URI`](https://developer.android.com/reference/android/net/Uri) that defines where the mesh lives. This URI determines whether the mesh is a local file, a networked file, or a custom object.
- `hittable`: Either `LineTest` or `NoCollision`. These specify whether the mesh should block rays (like controller pointers) cast through the scene. If you include `NoCollision`, rays will pass through the mesh.
- `defaultShaderOverride`: The string path to optionally override which shader the model uses. By default, Spatial SDK uses a physically-based rendering shader.
- `defaultSceneOverride`: The index to optionally override which scene you want to load. If not specified, the Mesh class will load the [default scene](https://github.khronos.org/glTF-Tutorials/gltfTutorial/gltfTutorial_004_ScenesNodes.html#scenes).

### The URI

Spatial SDK supports multiple protocols for pointing a URI to a mesh. The `mesh://` protocol is the primary one, but you can use any of the following protocols:

- `mesh://`: Use a custom mesh creator to load your object.
- `file://`: Load a [glTF/glb](/documentation/spatial-sdk/spatial-sdk-gltfs/) file from the given absolute file path.
- `apk://`: Load a [glTF/glb](/documentation/spatial-sdk/spatial-sdk-gltfs/) file relative to the assets folder of your Spatial SDK app.
- `http://` and `https://`: Load the `glb` file from the given networked URL. You must use [OkHTTP](/documentation/spatial-sdk/spatial-sdk-spatialfeature/) to support the `https://` protocol
  - This is an experimental feature.
- No protocol specified: Spatial SDK will attempt to read your local mesh file relative to your assets directory (similar to `apk://`).

## The `mesh://` protocol

The `mesh://` protocol enables you to define custom meshes parameterized by runtime values. For example, `mesh://sphere` loads a sphere mesh with a radius defined by the attached `Sphere(radius: Float)` component and the material defined by the `Material` component.

```
// create a blue sphere with radius 2
Entity.create(
    listOf(
        Mesh(Uri.parse("mesh://sphere")),
        Sphere(2.0f),
        Material().apply {
            baseColor = Color4(blue=1.0f)
        }
    )
)
```

Out of the box, Spatial SDK supports these meshes using the `mesh://` protocol:

- `mesh://plane`: Uses the `Plane(width: Float, depth: Float)` to create a plane with the given `width x 0.1 x depth` dimensions.
- `mesh://sphere`: Uses `Sphere(radius: Float)` to create a sphere mesh with the given `radius`.
- `mesh://box`: Uses `Box(min: Vector3, max: Vector3)` to create a rectangular prism, with one corner at the `min` point and the opposite corner at the `max` point.
- `mesh://roundedbox`: This mesh is the same as `mesh://Box` but uses `RoundedBox(min: Vector3, max: Vector3, radius: Vector3)` with a `radius` to apply rounding to the edges of the box.
- `mesh://dome`: Creates a half sphere that is 1 km in radius.
- `mesh://axis`: Create an RGB XYZ axis, which is useful for debugging which direction is up, forward, and down.
- `mesh://skybox`: Creates an entire sphere with a 1 km radius.

### Registering custom `mesh://`s with `registerMeshCreator`

Spatial SDK offers several meshes that serve as essential primitives. However, you can register custom meshes with the `registerMeshCreator` function.

```
// in the app's onCreate()
registerMeshCreator("mesh://floor") {
    SceneMesh.box(
        -5f,
        -0.1f,
        -5f,
        5f,
        0f,
        5f,
        // load a grass texture that's already set up
        SceneMaterial(SceneTexture(getDrawable(R.drawable.Grass_02)))
    )
}
```

This example loads a floor mesh, a thin 10 x 10 square with a grass texture. Spatial SDK will load this mesh whenever you specify a mesh with the `mesh://floor` URI. Spatial SDK provides a static mesh, but since `registerMeshCreator` takes a function, you can select any custom implementation or dependencies on custom components.

## Loading glTF/glb files

See the [glTFs](/documentation/spatial-sdk/spatial-sdk-gltfs/) page for more information about glTF/glb files.

Put your gITF/glb files in your assets folder and use the following code to load your models.

```
Entity.create(
    listOf(
        Mesh(
          Uri.parse("mymodel.glb")
        )
    )
)
```

## Transformations

You can control the translation and rotation of an `Entity` by using the `Transform` component. This allows you to set a pose, which contains a `Vector3` and `Quaternion`. The `Vector3` represents the translation in xyz space, while the quaternion represents the rotation.

If you wanted to create a glb model at point (1, 2, 3) and rotate it 180 degrees around the entity's local y-axis, you could create it like this:

``` kotlin
Entity.create(
    listOf(
        Mesh(Uri.parse("mymodel.glb")),
        Transform(Pose(Vector3(1f, 2f, 3f), Quaternion(0f, 180f, 0f)))
    )
)
```

## TransformParent

The `TransformParent` component allows us to set the transform entity to be local to another entity. For example, if you have an entity that represents the Earth and another entity that represents the Moon, then as the Earth entity moves, you would want the Moon entity to stay in the same place relative to the Earth (ignore the Moon's orbit for now). To do this, you can set the `TransformParent` component on the Moon to be the Earth entity.

``` kotlin
val earth = Entity.create(
                listOf(
                    Mesh(Uri.parse("earth.glb")),
                    Transform(Pose(Vector3(1f, 2f, 3f)))
                )
            )
val moon = Entity.create(
                listOf(
                    Mesh(Uri.parse("moon.glb")),
                    TransformParent(earth)
                    // Note: This is a transform local to the Earth's transform (1, 2, 3)
                    Transform(Pose(Vector3(1, 0, 0)))
                )
            )
```

This code creates an Earth entity and a Moon entity. Because the Moon entity has the `TransformParent` component set, the Moon entity's `Transform` is set as a local transform to the Earth entity's transform. In this example, the Earth would be at world coordinates (1, 2, 3), and the Moon would be at world coordinates at (2, 2, 3).

If the Earth entity has its transform changed, the Moon will also be changed so that its local transform to the Earth remains unchanged. You can also change the Moon's transform, and it will change to the new local position relative to the Earth.

To remove a `TransformParent` and have an entity use a normal absolute transform, you can set the `TransformParent` to be the `nullEntity`.

``` kotlin
// set the TransformParent
myEntity.setComponent(TransformParent(myParentEntity))
...
// remove the TransformParent
myEntity.setComponent(TransformParent(Entity.nullEntity()))
```

## Scaling meshes

You can use the `Scale` component to scale a mesh or a panel. This component will scale the mesh uniformly in the x, y, and z directions, and you can change this scale at any time.

glTF models often use centimeters instead of meters, which is the wrong scale. This mismatched scaling frequently requires you to add `Scale(Vector3(0.01f))` to your mesh if the mesh is too big.

```
Entity.create(
    listOf(
        Mesh(Uri.parse("mymodel.glb")),
        Scale(Vector3(3.5f, 1f, 1f))
    )
)
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-android-studio-plugin.md
---
title: Meta Horizon Android Studio plugin
description: Learn how to set up the Spatial SDK Android Studio plugin, and learn about its features.
last_updated: 2025-04-08
---

This Meta Horizon Android Studio Plugin is designed to enhance the experience of Android developers building for Horizon OS. It provides project templtes, a data model inspector, and component/system file templates.

## Install the Meta Horizon Android Studio Plugin

To install the Meta Horizon Android Studio Plugin, follow these steps.

1. In Android Studio, click **File** > **Settings** > **Plugins**.

2. In the **Plugins** window, click **Marketplace**.

3. In the search bar, type _Meta Horizon_ and select the **Meta Horizon** plugin.

4. If prompted, restart Android Studio.

    The plugin appears as the Meta logo on the right toolbar of Android Studio.

## Features
### Project templates

Using project templates, you can create a new Spatial SDK project. To use project templates in Android Studio, follow these steps.

1. In Android Studio, click **File** > **New** > **New Spatial SDK Project**.

    The **New Project** window appears.

2. Fill out the fields, and then click **Create**.

    Your new Spatial SDK project opens. It may take a few minutes to sync Gradle.

### Data Model Inspector

Debug your scene with the [Data Model Inspector](/documentation/spatial-sdk/spatial-sdk-tooling-dmi/).

### Component and System file templates

Component and System file templates help you create new components and systems. To use the file templates in Android Studio, follow these steps.

1. In the file directory of your Android Studio project, right-click on the folder that should contain the new file, and then select either **New** > **Spatial SDK Component** or **New** > **Spatial SDK System**.

    A window appears and prompts to name the template.

2. Type a name, and then press the **Enter** key.

    A new file is added to the folder and automatically opens.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-animations.md
---
title: Animations
description: Meta Spatial SDK supports animating meshes via animation data stored in gltf files.
last_updated: 2024-11-25
---

## Overview

Spatial SDK supports many types of animation, enabling you to add rich animated content to your apps.

You can animate your content in various ways:
- Use animation data stored in [glTF](/documentation/spatial-sdk/spatial-sdk-gltfs/) files.
- Write a [system](/documentation/spatial-sdk/spatial-sdk-writing-new-system/) to animate meshes.
- Use Android's animators, such as [`ValueAnimator`](https://developer.android.com/reference/android/animation/ValueAnimator).

## glTF animations

glTF models support storing animation data about transforms in interpolatable keyframes.

### Sourcing animations

You can obtain animations from various sources. This section includes some of the more popular tools and services for getting or creating animations.

- Sketchfab

    [Sketchfab](https://sketchfab.com/) and other 3D asset websites will often have animations. On Sketchfab, you can filter by **Animated** to find these models specifically. You can switch between animations at the bottom of the Sketchfab viewer. The names of the animations should correspond with the `animationNameToTrack` property mentioned below.

- Mixamo

    [Mixamo](https://www.mixamo.com/) is an excellent place to rig and animate your characters, or browse through shared animations uploaded by others. As mentioned on the [glTF page](/documentation/spatial-sdk/spatial-sdk-gltfs), Mixamo doesn’t support glTF models yet. You must convert the `.fbx` files to the glTF format. You can use Blender or other software to do this conversion.

- Blender

    Besides re-exporting from Mixamo, you can create animations yourself using Blender. The [Blender manual](https://docs.blender.org/manual/en/latest/animation/introduction.html) has more information on animation. When exporting to glTF format, use the settings mentioned in the [Blender documentation](https://docs.blender.org/manual/en/2.80/addons/io_scene_gltf2.html#animation-tab) to ensure your exported files are correct.

### Loading animations

Before adding your animations in Spatial SDK, check them using a reference glTF viewer to ensure they are correct. You can use [Khronos’ glTF sample viewer](https://github.khronos.org/glTF-Sample-Viewer-Release/) and go to the **Animation** tab on the right-hand side to check that all your animations are there and play correctly.

### Controlling animations in a Meta Spatial app

After confirming that your animation data is in your glTF file and working correctly, you can import the animation into your scene using the `Animated` component and a mesh component:

```
class Animated(
    startTime: Long,
    pausedTime: Float = 0.0f,
    playbackState: PlaybackState = PlaybackState.PLAYING,
    playbackType: PlaybackType = PlaybackType.LOOP,
    track: Int = 0
)
```

For simple use cases, you can play an infinitely looping animation.

```
// assuming you already have a Mesh component on myEntity
myEntity.setComponent(Animated(System.currentTimeMillis()))
```

Here is a breakdown of the arguments:

- `startTime`: This is the [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) (milliseconds) of when you want your animation to start. The code example above sets the current system time so that the animation will start immediately.
- `pausedTime`: This is a floating point time in seconds representing the moment to display in the animation when you pause it.
- `playbackState`: Corresponds to the `PlaybackState` enum. Either `PLAYING` (default) or `PAUSED`.
- `playbackType`: Corresponds to the `PlaybackType` enum.
  - `LOOP` (default): Restarts the animation when it passes the end of the animation.
  - `CLAMP`: Freezes the model in the final pose of the animation at the end.
- `track`: The index of the animation track you want to play (the default is 0, which is the first track). You can utilize `SceneMesh.animationNameToTrack` to get a track ID using the track’s name.

## System animations

You can write a system to control the animations of meshes.

Here is an example of `AnimationSystem`:

```kotlin
class AnimationSystem() : SystemBase() {
  var previousTime: Long = 0L

  override fun execute() {
    if (previousTime == 0L) {
      previousTime = System.currentTimeMillis()
    }
    val currentTime = System.currentTimeMillis()
    val timeDeltaInSeconds = (currentTime - previousTime) / 1000.0f
    previousTime = currentTime
    val q = Query.where { has(AComponent.id) }
    for (entity in q.eval()) {
      val tf = entity.tryGetComponent<Transform>() ?: continue
      tf.transform.t.y = tf.transform.t.y + 0.01f * timeDeltaInSeconds
      entity.setComponent(tf)
    }
  }
}
```

To use `AnimationSystem`, register it in your application:

```kotlin
class TestActivity : AppSystemActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    systemManager.registerSystem(AnimationSystem())
  }
}
```

After running the app, scene objects that have an `AComponent` will move up 1 cm every second.

## Android animations

Android provides a number of tools to support animations in Android applications. For example, you can use `ValueAnimator` to animate meshes.

Here is an example that demonstrates how to animate the scaling of an object from zero to its full size using `ValueAnimator`:

```kotlin
ValueAnimator.ofFloat(0f, 1f)
    .apply {
      duration = 1000
      interpolator = OvershootInterpolator(1f)
      addUpdateListener { animation ->
        val v = animation.animatedValue as Float
        entity.setComponent(Scale(scale.scale.multiply(v)))
      }
    }
    .start()
```

This code snippet starts an animation that scales a scene object from zero to its original size over a period of one second.

For more information on how to make Android animations, see the official Android [Introduction to animations](https://developer.android.com/develop/ui/views/animations/overview) page.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-architecture.md
---
title: Spatial SDK Architecture
description: Architecture page for Meta Spatial SDK first access doc site.
last_updated: 2024-10-16
---

Spatial SDK is a framework that provides XR capabilities such as graphics, input, and audio. Spatial SDK integrates with common and critical Android frameworks like Android UI and JetPack Compose. The framework makes it easy for developers familiar with Android to build immersive experiences without learning a new set of tools or frameworks. By leveraging existing Android knowledge, Spatial SDK can provide a more intuitive development experience while delivering powerful XR capabilities.

## Spatial SDK's architecture in the Android ecosystem

Spatial SDK's architecture fits within the existing Android ecosystem, meaning that SDKs components sit on top of Android components like Activities, Fragments, and Views. The SDK leverages Android's strengths and augments them to offer a unique set of XR capabilities.

## Core modules of Spatial SDK

Spatial SDK comprises several core modules that work in tandem to offer XR capabilities. These modules include graphics, input, and audio. Each module is reusable, allowing you to select the features needed for your specific application.

## App architecture

Creating a new activity for XR is recommended. This activity should inherit from [`AppSystemActivity`](/documentation/spatial-sdk/api-reference/latest/root/com.meta.spatial.toolkit/app-system-activity/). You can also reference multiple activities if needed. For instance, you might have a main activity that hosts a 3D scene, and another that displays a settings menu. Creating a new activity for each screen helps organize your code and create a more modular application. Additionally, referencing multiple activities enables code reuse beyond Meta Quest devices.

## Entity Component System architecture

The core of the Spatial SDK is the [Entity-Component-System (ECS)](/documentation/spatial-sdk/spatial-sdk-ecs/) architecture pattern. ECS separates data and execution. Entities can have multiple components as well as systems that operate on those components. This is a software pattern that uses composition over inheritance.

An entity is a unique identifier for a specific object in your app. It has no associated data and can have multiple components attached to it. For example, a player entity might have `transform`, `health`, and `score` components. Components hold the data for a specific aspect of an entity.

Components can hold simple or complex types of data, and they must be serializable. For example, a position component might hold `x, y, z` coordinates as floats for an entity.

Systems execute on data in your app. Systems use queries to retrieve the data they need to operate on. For example, a collision detection system might query all entities with a `collidable` component and check their positions to determine if any collisions have occurred.

This architecture pattern allows for greater composition, flexibility, and modularity in your code, making it easier to maintain and scale.

## DataModel

The [`DataModel`](/reference/spatial-sdk/latest/root/com.meta.spatial.core/data-model/) is fundamental to Spatial SDK’s design. It is a key-value store for caching and storing data. Queries retrieve data from the `DataModel`. The `DataModel` is flexible and scalable, allowing developers to store and retrieve data in various ways. Additionally, the `DataModel` retrieves and manipulates data within its entities and components. Using this key-value store, developers can cache data for faster access and store data in a way that is easy to query.

The `DataModel` provides first-class replication support. Developers can use this support to create multiplayer applications, like a meeting application that supports Avatars and VOIP.

## Data queries

Queries allow you to retrieve specific data from the `DataModel` based on certain criteria. For example, you might query all entities with a `player` tag to retrieve a list of all players in your application. Queries can be simple or complex, allowing developers to retrieve the data needed for their applications. By using queries, developers can filter data, making it easier to execute only the relevant information for the system. Queries are powerful tools that help developers build more dynamic and responsive applications.

## The scene

### SceneMesh

The 3D representation of an object in the scene is known as a [`SceneMesh`](/reference/spatial-sdk/latest/root/com.meta.spatial.runtime/scene-mesh/). GLTF files are the primary way to set up a `SceneMesh`. These files contain information about the object’s geometry, materials, and animations. Using GLTF files, developers can import and export 3D models into their applications.

### SceneObject

An instance of a `SceneMesh` is known as a [`SceneObject`](/reference/spatial-sdk/latest/root/com.meta.spatial.runtime/scene-object/). You create `SceneObject`s via the Creator Systems from the `DataModel`. You can create and manage multiple instances of the same `SceneMesh` within your application to create more complex and dynamic scenes.

### PanelSceneObject

[`PanelSceneObject`](/reference/spatial-sdk/latest/root/com.meta.spatial.runtime/panel-scene-object) is the 3D scene object responsible for displaying the 2D UI. This object allows developers to create interactive and immersive user interfaces within their 3D scenes. By combining 2D UI elements with 3D objects, developers can create more engaging and intuitive user experiences.

## UI and Spatial SDK

Spatial SDK is neutral about the UI technology you use. The close collaboration between the UI system and the `DataModel` matters more. Spatial SDK supports Android UI and Jetpack Compose. You can also integrate React Native. You can implement an activity based on Spatial SDK in addition to your current mobile applications, allowing you to gradually adopt XR capabilities into your existing app.

### Activities

Spatial SDK can host the UI within the same activity as a 3D Scene. Spatial SDK can also host 2D Activities, allowing the Spatial SDK Activity to work alongside apps to allow for gradual adoption. By using activities, you can create more modular and maintainable code while still leveraging Spatial SDK’s XR capabilities.

You cannot use multiple instances of the `AppSystemActivity` within a single app.

### Input

An [`InputSystem`](/reference/spatial-sdk/latest/root/com.meta.spatial.vr/input-system) converts controller input into interactions on the 2D panel. Spatial SDK supports hands and controllers. By supporting multiple input methods, Spatial SDK makes it easier for you to create accessible and intuitive user interfaces.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-attributes.md
---
title: Attributes
description: An explanation of the attributes that are available to devs
last_updated: 2025-04-17
---

## Overview

Attributes are at the core of Spatial SDK's [data model](/documentation/spatial-sdk/spatial-sdk-architecture#datamodel). They represent serializable data units that can be stored and used inside of your components.

A component can contain many attributes. For example, the `Grabbable` component contains:

```xml
<BooleanAttribute
  name="enabled"
  defaultValue="true"
  description="Defines whether the object can be grabbed or not."
/>
<EnumAttribute
  name="type"
  defaultValue="GrabbableType.FACE"
  description="The type of behavior an object has when grabbed (faces user, pivots on y axis, etc.)"
/>
<BooleanAttribute
  name="isGrabbed"
  defaultValue="false"
  description="Whether the object is currently grabbed or not"
/>
<FloatAttribute
  name="minHeight"
  defaultValue="-Float.MAX_VALUE"
  description="the minimum height an object can be held when grabbed"
/>
<FloatAttribute
  name="maxHeight"
  defaultValue="Float.MAX_VALUE"
  description="the maximum height an object can be held when grabbed"
/>
```

The build process will generate Kotlin code and Android resources based on the XML inputs.

## Supported attributes
- Spatial SDK currently support below attributes:

    {%include spatial-sdk-shared/spatial-sdk-shared-attributes.md %}

Some attributes are self-explanatory by name. For example, `IntAttribute` is a 32 bit integer. Other attributes require more explanation. This document describes the available attributes one-by-one.


### `Color4Attribute`

`Color4Attribute` can be used to store colors. You can use either a hex string or a comma-separated list of four floats(r,g,b,a) to define the color.

```xml
<Color4Attribute name="color" defaultValue="1.0f, 0.0f, 0.0f, 1.0f" />
<Color4Attribute name="colorHex" defaultValue="#112233FF" />
```

### `EntityAttribute`

`EntityAttribute` represents a reference to another entity in Spatial SDK's [ECS](/documentation/spatial-sdk/spatial-sdk-ecs). The Entity is represented by a long integer under-the-hood and is recontructed on creation for use. All entity attribute will have a default value of `Entity.nullEntity()`.

```xml
<EntityAttribute name="target" description="Target Entity to follow" />
```

### `EnumAttribute`

You must specify a valid Kotlin enum value to the `defaultValue` XML property of `EnumAttribute`. The enum value can be defined in XML or Kotlin.

```xml
<Enum
  name="GrabbableType"
  description="GrabbableType is an enum that defines the type of behavior an object has when grabbed. "
>
  <EnumValue
    value="FACE"
    description="The object faces the user when grabbed."
  />
  <EnumValue
    value="PIVOT_Y"
    description="The object will be pivoted in Y dimension."
  />
</Enum>
<Component name="Grabbable">
  <EnumAttribute
    name="type"
    defaultValue="GrabbableType.FACE"
    description="The type of behavior an object has when grabbed (faces user, pivots on y axis, etc.)"
  />
</Component>
```

Enum attributes can be set and retrieved as the enums they represent. Here is an example:

```kotlin
  Grabbable(type = GrabbableType.PIVOT_Y ...
```

### `ExperimentalMapAttribute`

```xml
<ExperimentalMapAttribute name="lines" keyType="Int" valueType="Vector3" description="Represents the lines on a whiteboard" />
```

`ExperimentalMapAttribute` is a Kotlin map with a limited API. Currently our maps support `get`, `set`, `contains`, and `remove`.

Valid key types include `Int`, `Long`, and `String`. Valid value types include `Int`, `Long`, `Float`, `String`, `UUID`, `Vector2`, `Vector3`, `Vector4`, `Quaternion`, and `Pose`. (Note: `UUID`, `Pose` and `Quaternion` are not supported by the Spatial Editor to display and edit.)

`ExperimentalMapAttribute` supports about 30 elements (depending on your app load) before performance slows. If you need to improve performance, APIs are available on the entity for direct data access and modification.

```kotlin
  inline fun <reified T, reified V> getMap(attribute: Int): HashMap<T, V>
  inline fun <reified T, reified V> tryGetMapValue(attribute: Int, key: T): V?
  inline fun <reified T, reified V> trySetMapValue(attribute: Int, key: T, value: T): Boolean
  fun setMap(attribute: Int, value: HashMap<*, *>)
  fun addToMap(attribute: Int, value: HashMap<*, *>)
```

### `FloatAttribute, BooleanAttribute, IntAttribute, LongAttribute`

These are all native Kotlin objects. The names all indicate the types you you can expect: `Float`, `Boolean`, `Int`, `Long`.

```xml
<FloatAttribute
  name="tolerance"
  defaultValue=".2f"
  description="This is the change in distance needed to start moving"
/>
<BooleanAttribute
  name="active"
  defaultValue="true"
  description="Whether entity is actively following or not"
/>
<IntAttribute
  name="track"
  defaultValue="0"
  description="which animation track of the glTF to play"
/>
<LongAttribute
  name="startTime"
  defaultValue="-1L"
  description="World time at which animation started (ms since epoch)"
/>
```

**FloatAttribute**

You have to set a valid Kotlin float value to the `defaultValue` property of a `FloatAttribute`. In Kotlin, `1.1` is a `Double`, not a `Float`. If no `defaultValue` is specified, it will fall back to `0.0f`.

You can also specify a range for the `FloatAttribute` using the `Constraints` tag. The `Min` and `Max` tags are required. The `Min` tag must be less than or equal to the `Max` tag.

```xml
<FloatAttribute name="floatAttr" defaultValue="-.1f" />
<FloatAttribute name="floatAttr1" description="no defaultValue provided, this attribute will have a default value of 0.0f" />
<FloatAttribute name="floatAttrWithRange" defaultValue="0.0f">
  <Constraints>
    <Min>-10.0f</Min>
    <Max>10.0f</Max>
  </Constraints>
</FloatAttribute>
```

**IntAttribute**

You have to set a valid Kotlin Int value to the `defaultValue` property of an `IntAttribute`. If no `defaultValue` is specified, it will fall back to `0`.

You can also specify a range for the `IntAttribute` using the `Constraints` tag. The `Min` and `Max` tags are required. The `Min` tag must be less than or equal to the `Max` tag.

```xml
<IntAttribute name="intAttr" defaultValue="1" />
<IntAttribute name="intAttr1" description="no defaultValue provided, this attribute will have a default value of 0" />
<IntAttribute name="intAttrWithRange" defaultValue="0">
  <Constraints>
    <Min>-10</Min>
    <Max>10</Max>
  </Constraints>
</IntAttribute>
```
**LongAttribute**

You have to set a valid Kotlin Long value to the `defaultValue` property of a `LongAttribute`. If no `defaultValue` is specified, it will fall back to `0L`.

You can also specify a range for the `LongAttribute` using the `Constraints` tag. The `Min` and `Max` tags are required. The `Min` tag must be less than or equal to the `Max` tag.

```xml
<LongAttribute name="longAttr" defaultValue="1L" />
<LongAttribute name="longAttr1" description="no defaultValue provided, this attribute will have a default value of 0L" />
<LongAttribute name="LongAttrRange" defaultValue="100">
  <Constraints>
    <Min>-10</Min>
    <Max>10</Max>
  </Constraints>
</LongAttribute>
```
### `PoseAttribute`

`PoseAttribute` is a commonly used attribute to represent a 3D position and orientation. The transform component only has one attribute, a pose. These are stored and created as Spatial SDK poses (`com.meta.spatial.core.Pose`).

```xml
<PoseAttribute name="transform" description="Represents the position and orientation of an object" />
```

For a `PoseAttribute`, you must specify a valid pose as the `defaultValue`. A pose contains position and orientation data.

```xml
<PoseAttribute name="poseAttr" defaultValue="1f,2f,3f,4f,5f,6f,7f" />
```
As shown above, the first three floats, `1f,2f,3f`, represent the position of a pose in the form of a Vector3. The the last four digits, `4f,5f,6f,7f`, represent the orientation in the form of a quaternion. If no `defaultValue` is specified, it will fall back to `0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f`.
### `UUIDAttribute`

`UUIDAttribute` can be used to store a Java UUID (`java.util.UUID`). UUIDs are 128 bit data stores that are commonly used for database keys, transaction ids, and more.

For a `UUIDAttribute`, you can provide a valid UUID string as the `defaultValue`. If no `defaultValue` is provided, a random UUID will be used.

```xml
<UUIDAttribute name="uuidAttr" defaultValue="123e4567-e89b-12d3-a456-426614174000" />
```

You can also specify the most significant bit (MSB) and the least significant bit (LSB) of a UUID.

```xml
<UUIDAttribute name="uuidAttr" defaultValue="-2, 1L" />
```

The above `UUIDAttribute` has a UUID default value of `java.util.UUID(-2L, 1L)`.

### `URIAttribute`

`URIAttribute` can be used to store a URI (`android.net.Uri`). A URI is a string that represents a resource. The given URI must be a valid URI otherwise Spatial SDK project build will fail with an IllegalArgumentException.

```xml
<URIAttribute name="uriAttr" defaultValue="http://www.meta.com" description="URI attribute"/>
```

### `Vector2Attribute, Vector3Attribute, Vector4Attribute`

These store Spatial SDK's `Vector2Attribute`, `Vector3Attribute`, and `Vector4Attribute` (`com.meta.spatial.core.VectorNAttribute`). The [API documentation](/reference/spatial-sdk/latest) provides details on these types, including built-in functions for multiplication and addition.

```xml
<Vector2Attribute
  name="dimensions"
  defaultValue="0.75f, 1.0f"
  description="used to store the panel dimensions" />
<Vector3Attribute
  name="followOffset"
  defaultValue="0f, 0f, 0f"
  description="used to define the location that the followable tracks to" />
  /**  */
<Vector4Attribute
  name="baseColorInternal"
  defaultValue=".5f, .5f, .5f, 1.0f"
  description="holds material base colors, accessed through a getter" />
```

**Vector2Attribute**

The `defaultValue` for a `Vector2Attribute` should be a pair of float values representing a 2D vector. If you don't set the defaultValue, it will fall back to 0.0f, 0.0f.

```xml
<Vector2Attribute name="vector2Attr" defaultValue="0.1f,0.0f" />
```

**Vector3Attribute**

For a `Vector3Attribute`, the `defaultValue` should be three float values representing a 3D vector. If you don't set the `defaultValue`, it will fall back to `0.0f,0.0f,0.0f`.

```xml
<Vector3Attribute name="vector3Attr" defaultValue="0.0f,0.0f,1.0f" />
```

**Vector4Attribute**

The `defaultValue` for a `Vector4Attribute` must be four float values representing a 4D vector. If you don't set the defaultValue, it will fall back to `0.0f,0.0f,0.0f,0.0f`.

```xml
<Vector4Attribute name="vector4Attr" defaultValue="0.0f,0.0f,0.0f,1.0f" />
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-audio.md
---
title: Audio
description: Play audio using Android’s or Meta Spatial SDK's native audio APIs.
last_updated: 2024-12-04
---

## Overview

This document covers playing audio using Android’s or Spatial SDK's native audio APIs.

## Supported audio types

### File Types
`.wav` and `.ogg` audio files are supported.

### Sample Rate
- 48kHz is typically used, but any common multiple of 16kHz should work (for example, 32kHz, 48kHz, 96kHz).
- 44.1kHz audio is not supported at this time.

### Encoding
`Signed 16-bit PCM` for `.wav` files is supported.

## `Audio()` component

You can add audio components to entities to play spatialized audio for each entity. The file string is parsed by `SceneAudioAsset`, as explained below, and the `AudioSystem()` plays it.

```kotlin
class Audio(
    file: String,
    volume: Float = 1.0f,
) : ComponentBase()
```

## `SceneAudioAsset`

Your scene can have many sounds associated with a single `SceneAudioAsset`. Use `SceneAudioAsset` to efficiently reuse audio resources in your application.

Spatial SDK imposes restrictions on asset usage, including what types of audio can be spatialized. The `SceneAudioAsset` class enforces these checks. To use spatial audio, ensure your sound file is mono. Stereo sound files cannot be spatialized.

```kotlin
public class SceneAudioAsset(filepath: String) {
    val canBeSpatialized: Boolean
    val duration: Float
}
```

Here is an example:

```kotlin
val SFX_SELECT = SceneAudioAsset("shopping/SFX_Select.wav")
```

## Play a one-shot sound from a specific position

You can play sounds from a specific origin within your scene, and use the player's position to determine how it should sound relative to where they are.

```kotlin
public class SceneAudioPlayer(scene: Scene, audioAsset: SceneAudioAsset) {
    fun play(position: Vector3, volume: Float = 1.0f, looping: Boolean = false)
    fun setPosition(position: Vector3)
    fun stop()
}
```

To play a sound at a specific position, the `SceneAudioAsset` must be spatializable. Ensure the `canBeSpatalized` property is true. Otherwise, the audio will be played but won't be localized to a point.

```kotlin
class SpatialAudioActivity : AppSystemActivity() {

  override fun onSceneReady() {
    super.onSceneReady()

    val audioPlayer = SceneAudioPlayer(scene, SceneAudioAsset("audio/click.wav"))

    val entity =
        Entity.create(...)

    entity?.registerEventListener<ButtonReleaseEventArgs>(ButtonReleaseEventArgs.EVENT_NAME) {
        entity,
        eventArgs ->
      if (eventArgs.button == ControllerButton.RightTrigger) {
        audioPlayer.play(entity?.GetPosition())
      }
      else if (eventArgs.button == ControllerButton.LeftTrigger) {
        audioPlayer.setPosition(entity?.GetPosition() + Vector3(1.0f, 0.0f, 0.0f))
    }
  }
}
```

## Play a one-shot sound

You may need to play a single sound to completion. Spatial SDK supplies simple APIs to allow one-shot sounds to play.

```kotlin
class Scene {
…
    fun playSound(soundAsset: SceneAudioAsset, volume: Float)
    fun playSound(soundAsset: SceneAudioAsset, position: Vector3, volume: Float)
…
}
```

The sound will play to completion. You will not be able to cancel the playback early.

Here is an example:

```
scene.playSpatialSound("audio/click.wav", 1f, hitInfo.point)
```

```kotlin
class SpatialAudioActivity : AppSystemActivity() {

  override fun onSceneReady() {
    super.onSceneReady()


    val soundAsset = SceneAudioAsset("audio/click.wav")

    val entity =
        Entity.create(...)

    entity?.registerEventListener<ButtonReleaseEventArgs>(ButtonReleaseEventArgs.EVENT_NAME) {
        entity,
        eventArgs ->
      if (eventArgs.button == ControllerButton.RightTrigger ||
          eventArgs.button == ControllerButton.LeftTrigger) {
        playSound(soundAsset, entity?.GetPosition(), 1.0f)
      }
    }
  }
}
```

## Play a looping background sound

Background sounds support spatial audio but are not spatialized. Only one background sound can be played at a time.

```kotlin
class Scene {
…
    fun playBackgroundSound(soundAsset: SceneAudioAsset, volume: Float, looping: Boolean)
…
}
```

### Stop the background sound

To turn off the background sound in your app, use the following code:

```
class Scene {
…
    fun stopBackgroundSound()
…
}
```

## Android APIs

You can use Android audio APIs in your app without any issues. For example, Android `VideoView` will work out of the box, and audio plays when you call `.start()`.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-component.md
---
title: Write a new component
description: A Meta Spatial SDK tutorial on writing a new component.
last_updated: 2025-04-17
---

## Overview

Components serve as the core of Spatial SDK’s data store. They are networked by default and embody the data shared across various instances of an app. Entities are long IDs that bundle components together. It's recommended that you reuse components across entities.

## Creating a new component

Components are intended to be pure attribute containers. Starting from v0.5.5, you can define a component using an XML file, such as one named `component.xml`, for example. When you build your app, the Gradle plugin will pick up the XML files under `app/src/main/components` to generate Kotlin code first. It then compiles the entire project with the generated Kotlin code. The file can have any name as long as it is unique and inside `app/src/main/components`. If you need to define multiple components, you can either define multiple components within the same file or create multiple files.

1. Create a component XML file:

    In your project directory, create a new XML file under `app/src/main/components/`. You can name it anything, such as `component.xml`.
2. Define the Component Schema:

   Use the `<ComponentSchema>` tag to specify the package name. Note that the package name has to match the package name you specify in your Android manifest or the `namespace` property in your `build.gradle.kts` file. Using a different package name will lead to build errors.
   ```xml
   <ComponentSchema packageName="your.package.name">
   </ComponentSchema>
   ```
3. Define enums (optional):

   You can define enums using component XMLs. You won't be able to see the enums in the Spatial Editor if you define them in Kotlin.
   ```xml
   <ComponentSchema packageName="your.package.name">
     <Enum name="TestEnum">
       <EnumValue value="FIRST" />
       <EnumValue value="SECOND" />
     </Enum>
   </ComponentSchema>
   ```
   The above code will generate the following Enum class:
   ```kotlin
   package your.package.name

   enum class TestEnum {
     FIRST,
     SECOND
   }
   ```
4. Define a Component:

   Within the `<ComponentSchema>`, use the `<Component>` element to define a new component. Each component can include multiple attributes. Inside the `<Component>` tag, you can define various attributes. Here is an example:

   ```xml
   <ComponentSchema packageName="your.package.name">
      <Enum name="TestEnum">
        <EnumValue value="FIRST" />
        <EnumValue value="SECOND" />
      </Enum>
      <Component name="TestComponent">
        <StringAttribute name="name" defaultValue="n/a" />
        <IntAttribute name="age" defaultValue="0" />
        <BooleanAttribute name="isActive" defaultValue="false" />
        <FloatAttribute name="height" defaultValue="0.0f" />
        <UUIDAttribute name="uniqueId" />
        <Vector3Attribute name="position" defaultValue="0.0f, 0.0f, 0.0f" />
        <EnumAttribute name="enumAttr" defaultValue="TestEnum.FIRST" />
        <ExperimentalMapAttribute name="attributesMap" keyType="String" valueType="Int" />
        <PoseAttribute name="poseAttr" />
      </Component>
   </ComponentSchema>
   ```

    The build process will generate Kotlin code in `build/generated/java` and resource files in `build/generated/res`.

5. Define attributes:

    Inside of the `<Component> </Component>` tag, you can define various attributes.

    {%include spatial-sdk-shared/spatial-sdk-shared-attributes.md %}

    **name and description XML properties**

    Each attribute tag includes a `name` XML property to specify the attribute's name. It also has a `description` property for adding a description or comments about the attribute.

    **defaultValue XML attribute**

    Most attributes require a `defaultValue`, except for `ExperimentalMapAttribute` and `EntityAttribute`. Ensure that the `defaultValue` is appropriate for the attribute type, following Kotlin conventions where applicable.

    You'll find more details on how to define attributes in [Attributes](/documentation/spatial-sdk/spatial-sdk-attributes/).

6. Define multiple components:

    To define multiple components, you can define multiple components within the same component XML file or use multiple XML files under `app/src/main/components`.

    You can define multiple components within a component XML like this:
    ```xml
    <ComponentSchema packageName="your.package.name">
      <Component name="TestComponent">
        ...
      </Component>
      <Component name="TestComponent1">
        ...
      </Component>
    </ComponentSchema>
    ````

7. Register components

    With your component ready, it’s time to register it so you can generate it as needed (this is how you use `entity.getComponent`). In your activity, add the following code to the `onCreate` hook:

    ```kotlin
    override fun onCreate(savedInstanceState: Bundle?) {
      super.onCreate(savedInstanceState)

      componentManager.registerComponent<TestComponent>(TestComponent.Companion)
    }
     ```

8. Use components

   You can now use your custom component.

    ```kotlin
    Entity.create(TestComponent())
    ```

## Specify the custom components folder

By default, the build process searches for XML files in the `app/src/main/components` folder. If you prefer to use a different folder for your custom components, you can edit `config.json` in `app/scenes/`.

```json
{
"spatial.editor.customComponentXmlsPath": [
    "../src/main/components/",
],
"spatial.editor.libraryComponentXmlsPath": "../build/generated/components"
}
```

To specify your desired folders, edit the paths in the `spatial.editor.customComponentXmlsPath` JSON property.

The Spatial Editor also uses `config.json` to find the custom components. You can find more information in [Create custom components](/documentation/spatial-sdk/spatial-editor-components#create-custom-components/).


## Specify the library components folder

By default, the build process exports XML components to `app/build/generated/components` from libraries such as `meta-spatial-sdk-toolkit`. The process looks for XML files within the `components` directories of each library. If you wish to use a different folder, you can edit `config.json` in `app/scenes/`. After that, the Spatial Editor will then read the exported XML files in `app/build/generated/components` to find the components.

**Note**: Do not modify the exported XML files, as they will be overwritten in the next build.

```json
{
  "spatial.editor.customComponentXmlsPath": [
      "../src/main/components/",
  ],
  "spatial.editor.libraryComponentXmlsPath": "../build/generated/components"
}
  ```

You can edit the path of the `spatial.editor.libraryComponentXmlsPath` JSON property to specify the folder you'd like to use.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-custom-shaders.md
---
title: Custom Shaders
description: Enhance your Meta Spatial SDK app's visuals with custom shaders.
last_updated: 2025-02-27
---

## Overview

**Note**: This is an advanced, experimental feature.

This page explains how to integrate your custom shaders with the Spatial SDK.

Shaders are programs on your graphics card that calculate vertex positions and pixel colors for geometry. By default in Spatial SDK, we use physically based shaders to create realistic graphics.

For most use cases, you can use the default, physically based shader, or choose from the many built-in shaders. For some advanced use cases, like performance optimization or custom effects, you may want to create your own shaders for your application.

## Shader pipeline

To begin developing your own shaders, it's helpful to understand the Spatial SDK shader pipeline. For each material, there is a pair of source shaders: the vertex (`.vert`) and fragment (`.frag`) shaders. The vertex shader computes the vertex locations of your geometry, and the fragment shader calculates the color of each pixel rendered.

These vertex and fragment source files are written in [OpenGL Shading Language (GLSL)](<https://www.khronos.org/opengl/wiki/Core_Language_(GLSL)>). The source files are compiled into a format that the graphics driver can interpret before you deploy your app using a program called [glslc](https://github.com/google/shaderc). Spatial SDK compiles these source shaders with many different configurations and loads them from your `assets` folder at runtime.

## Specifying shader overrides

By default, Spatial SDK uses a physically based shader found at `SceneMaterial.PHYSICALLY_BASED_SHADER`. This string value is defined as `"data/shaders/pbr/pbLit"`, which represents the path in the Android `assets` folder. This folder is also where compiled vertex and fragment shaders live (compiled from `pbLit.vert` and `pbLit.frag`).

Another built-in shader can be found at `SceneMaterial.UNLIT_SHADER`. This shader uses the model's base color without adding lighting or shadows. This shader is useful for enhancing performance, or for models with pre-baked lighting.

### Location strings

To use these shaders, you can specify location strings as arguments in a number of Spatial SDK APIs.

- In the `Mesh` component, specify a `defaultShaderOverride` to set the deafult shader for all materials loaded from the associated glTF.
  - If you want to change the shader of a specific material in your glTF, you can utilize the [extras](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#reference-extras) properties on your glTF material with the `"meta_spatial_sdk_shader"` key. For example, you can set a material shader to be unlit with the following key/value pair: `"meta_spatial_sdk_shader": "data/shaders/unlit/unlit"`.
- You can specify the shader on the `Material` component with the `shader` attribute. This lets you set the shaders for mesh creators like `mesh://box` and `mesh://sphere`.
- You can set the shader path directly on `SceneMaterial`, either in the constructor, or through a custom `SceneMaterial` (described later in this guide).
  - For advanced cases, use this to manage a direct reference to a material.

## Plugin setup

To use a custom shader, compile it with your app’s build process using our Meta Spatial Gradle Plugin. This plugin is used for many Spatial SDK features, like integration with [Meta Spatial Editor](/documentation/spatial-sdk/spatial-editor-overview/), [hot reloading](/documentation/spatial-sdk/spatial-sdk-hot-reload), and shader compilation. Apply it to your project as a plugin to use it.


After you apply the plugin, configure your `spatial` block:

```kotlin
// later in your build.gradle.kts
spatial {
   ...
   shaders {
        sources.add(
            // replace with your shader directory
            project.layout.projectDirectory.dir("src/shaders")
        )
    }
}
```

In our samples (for example, [MediaPlayerSample](https://github.com/meta-quest/Meta-Spatial-SDK-Samples/tree/main/MediaPlayerSample)), there is a custom directory in `app/src/shaders`. You can put your folders wherever you would like, as long as they are not in `app/src/main/shaders`, as this will conflict with some built-in Android Studio shader compilation.

If you try to build your app at this stage, you might get an error that the Native Development Kit (NDK) is not installed. This is because the Meta Spatial Plugin uses the glslc executable bundled with the Android NDK. Instructions for installing it can be found [here](https://developer.android.com/studio/projects/install-ndk).

Specify the NDK version you're using in your `android` block to ensure compatibility:

```kotlin
android {
   ...
   // use the version that was found on the "SDK Tools" window
   ndkVersion = "..."
}
```

To confirm everything works as expected, create two shader files.

1. Create the vertex shader at `src/shaders/myShader.vert`:

```c
#version 430
#extension GL_ARB_separate_shader_objects : enable
#extension GL_ARB_shading_language_420pack : enable

#include <metaSpatialSdkDefaultVertex.glsl>
```

2. Create the fragment shader at `src/shaders/myShader.frag`:

```c
#version 400
#extension GL_ARB_separate_shader_objects : enable
#extension GL_ARB_shading_language_420pack : enable

#include <metaSpatialSdkFragmentBase.glsl>

void main() {
  // simply write out a red color
  outColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
}
```

If you now build your app, your shaders should be compiled and packaged in your `assets` folder. You can then reference them in your app as `myShader`, which should make the rendered objects red.

## Shader interface

By default, shaders are assumed to be working off of the physically based material setup. With this setup, we have set up a pipeline to take base color, emissive, roughness/metallic, and other textures as well as other scalar parameters to render in a physically based way. If you want to build a shader off of these parameters, there are a number of files to help with authoring your shaders. Any file prefixed with `metaSpatialSdk` will be relative to the default material setup while others will be useful in any custom shader.

All material uniforms and attributes need to be specified to match the layout in the default `metaSpatialSdkDefaultVertex.glsl` shader example.

### app2vertex.glsl

This file gives access to the base vertex geometry, including positions, normals, and UV coordinates. To get access, you call `App2VertexUnpacked app = getApp2VertexUnpacked();`.

```kotlin
struct App2VertexUnpacked {
  // in object space
  vec3 position;
  // normalized, in object space
  vec3 normal;
  // material albedo color without texture in linear
  vec3 linearColor;
  // texture coordinate 0
  vec2 uv;

#if VERTEX_FORMAT_TWOUV == 1 || VERTEX_FORMAT_TWOUV_TANGENT == 1
  // texture coordinate 1
  vec2 u1;
#endif

#if VERTEX_FORMAT_TWOUV_TANGENT == 1
  // XYZ unit vector defining a tangential direction on the surface.
  // W component defines the handedness of the tangent basis (-1 or 1).
  vec4 tangent;
#endif

#if VERTEX_FORMAT_SKINNED == 1
  // For 4-bone skinning; each uint in the uvec4 specifies an index into a skinningMatrices array
  uvec4 jointIndices;
  // // For 4-bone skinning; each float in the vec4 specifies a weight used to weight the effect of the skinning matrix selected by jointIndices[i]
  vec4 jointWeights;
#endif
}

App2VertexUnpacked getApp2VertexUnpacked();
```

### Uniforms.glsl

This file gives you access to a struct of data that does not change throughout the rendering of all objects in a given frame including any object transformation matrices. You can access this data by including this file and using `g_ViewUniform` and `g_PrimitiveUniform`.

```c
struct ViewUniform {
  mat4 clipFromWorld0; // mono or left eye stereo
  mat4 clipFromWorld1; // right eye stereo
  vec4 eyeCenter0; // left eye location in world space, .w = 0
  vec4 eyeCenter1; // right eye location in world space, .w = 0
  vec4 random; // .x: random 0..1, .yzw: unused
  vec4 moduloTime; // modulus of time in sec. .x: mod 1sec, .y: mod 1min, .z: mod 1hour, w: unused
  uvec4 time; // .x: total time spent on rendering any scene in msec, .y: frame no, .zw: unused
  vec4 renderTargetSize; // .xy: size of render target width/height, .z: 1/width, w: 1/height
  vec4 viewParam1; // test variable that can be used in multiple places
  vec4 viewParam2; // test variable that can be used in multiple places
  ivec4 editorShaderData; // .x: editor shader visualization index.
  vec4 ambientColor; // .rgb: for simple lighting, .a:unused
  vec4 sunColor; // .rgb: for simple lighting, .a:unused
  vec4 sunDirection; // .rgb: for simple lighting, .a:unused
  vec4 environmentIntensity; // .x: intensity multiplier for IBL, .yzw: unused
  vec4 sh0; // .xyz: spherical harmonics coefficients used for diffuse IBL, .w:unused
  vec4 sh1; // .xyz: see sh0, .w:unused
  vec4 sh2; // .xyz: see sh0, .w:unused
  vec4 sh3; // .xyz: see sh0, .w:unused
  vec4 sh4; // .xyz: see sh0, .w:unused
  vec4 sh5; // .xyz: see sh0, .w:unused
  vec4 sh6; // .xyz: see sh0, .w:unused
  vec4 sh7; // .xyz: see sh0, .w:unused
  vec4 sh8; // .xyz: see sh0, .w:unused
  vec4 userParam0; //
  vec4 userParam1; //
  vec4 userParam2; //
  vec4 userParam3; //

} g_ViewUniform;

struct PrimitiveUniform {
  mat4 worldFromObject; // useful to transform positions from object to world  or  normals and tagents to object space
  mat4 objectFromWorld; // inverse of worldFromObject
} g_PrimitiveUniform;
```

### metaSpatialSdkMaterialBase.glsl

This file contains most of the scalar uniforms for your material setup. It will give you access to the `g_MaterialUniform` variable to access these values.

```c
uniform MaterialUniform {
  vec4 matParams; // x = roughness, y = metallic, z = unlit
  vec4 alphaParams; // x = minAlpha, y = cutoff
  vec4 stereoParams; // controls UV per eye, xy = eye 2 xy offset, zw = xy scale
  vec4 emissiveFactor; // multiplier for emissive texture
  vec4 albedoFactor; // multiplier for base color texture

  // used in the below transform functions
  vec4 albedoUVTransformM00;
  vec4 albedoUVTransformM10;
  vec4 roughnessMetallicUVTransformM00;
  vec4 roughnessMetallicUVTransformM10;
  vec4 emissiveUVTransformM00;
  vec4 emissiveUVTransformM10;
  vec4 occlusionUVTransformM00;
  vec4 occlusionUVTransformM10;
  vec4 normalUVTransformM00;
  vec4 normalUVTransformM10;
} g_MaterialUniform;

// can be used to get transformed texture UVs
vec2 getAlbedoCoord(vec2 uv);
float getAlbedoMix();

vec2 getRoughnessMetallicCoord(vec2 uv);
float getRoughnessMetallicMix();

vec2 getEmissiveCoord(vec2 uv);
float getEmissiveMix();

vec2 getOcclusionCoord(vec2 uv);
float getOcclusionMix();

vec2 getNormalCoord(vec2 uv);
float getNormalMix();
```

### metaSpatialSdkVertexBase.glsl

This file sets out the common output format from the vertex shader used by the fragment shaders (via `vertexOut`) as well as exposes bindings to a material uniform buffer used for skinning (in `g_StorageBuffer`).

```c
// includes from "common.glsl", "app2vertex.glsl", and "metaSpatialSdkMaterialBase.glsl"
out struct {
  vec4 color;
  vec2 albedoCoord;
  vec2 roughnessMetallicCoord;
  vec2 emissiveCoord;
  vec2 occlusionCoord;
  vec2 normalCoord;
  vec3 lighting;
  vec3 worldNormal;
  vec3 worldPosition;
#if VERTEX_FORMAT_TWOUV_TANGENT == 1
  vec4 tangent;
#endif
} vertexOut;

#if VERTEX_FORMAT_SKINNED == 1
readonly buffer StorageBuffer {
	mat4 skinningMatrices[];
} g_StorageBuffer;
#endif
```

### metaSpatialSdkFragmentBase.glsl

This file sets up all the material textures and inputs interpolated from the vertex shaders.

```c
// includes from "metaSpatialSdkMaterialBase.glsl"
// used for IBL
uniform sampler2D brdfLookup;
uniform samplerCube specularCubemap;
uniform sampler2DArray depth;

uniform sampler2D albedoSampler;
uniform sampler2D roughnessMetallicTexture;
uniform sampler2D emissive;
uniform sampler2D occlusion;
#if VERTEX_FORMAT_TWOUV_TANGENT == 1
uniform sampler2D normalMap;
#endif

in struct {
  vec4 color;
  vec2 albedoCoord;
  vec2 roughnessMetallicCoord;
  vec2 emissiveCoord;
  vec2 occlusionCoord;
  vec2 normalCoord;
  vec3 lighting;
  vec3 worldNormal;
  vec3 worldPosition;
#if VERTEX_FORMAT_TWOUV_TANGENT == 1
  vec4 tangent;
#endif
} vertexOut;

out vec4 outColor;

```

### metaSpatialSdkDefaultVertex.glsl

This sets up a vertex shader if you don’t want to rewrite your own. It is recommended to avoid re-implementing operations like joint skinning.

Putting all of these together, you can write a simple fragment shader that changes the colors of a model as you move it around like so:

```c
#version 400
#extension GL_ARB_separate_shader_objects : enable
#extension GL_ARB_shading_language_420pack : enable

#include <metaSpatialSdkFragmentBase.glsl>
#include <Uniforms.glsl>

void main() {
    vec4 pixel = texture(albedoSampler, vertexOut.albedoCoord) * vertexOut.color;
    float alphaCutoff = g_MaterialUniform.alphaParams.y;
    if(pixel.a < alphaCutoff){
       discard;
    }
    // tint the object based on it's position in the world
    outColor.xyz = pixel.xyz * sin(vertexOut.worldPosition.xyz * 10.0f);
    outColor.a = pixel.a;
}
```

## Custom materials

Sometimes, you may want to specify custom inputs and you don’t need the whole physically based material setup. For these cases you can use custom `SceneMaterial`s. Below is an example roughly lifted from our MediaPlayer sample. Please check out the sample for full implementation details.

```kotlin
val myMaterial = SceneMaterial.custom(
    "data/shaders/custom/360",
    arrayOf<SceneMaterialAttribute>(
        // define the some standard material attributes.
        SceneMaterialAttribute("albedoSampler", SceneMaterialDataType.Texture2D),
        SceneMaterialAttribute("stereoParams", SceneMaterialDataType.Vector4),
        // define the custom material attributes.
        SceneMaterialAttribute("customParams", SceneMaterialDataType.Vector4)
))

// update a value
myMaterial.apply {
    // set to texute red
    setTexture("albedoSampler", SceneTexture(Color.valueOf(1f, 0f, 0f, 1f)))
    setAttribute("customParams", Vector4(1.0f, 0f, 0f, 0f))
}
```

Currently, we support vector4 and texture material definitions in your custom materials. For how these translate to the shaders, check out the implementation of the vertex and fragment shaders.

```c
// in data/shaders/custom/360.vert
...
// vec4s are stored in set 3, binding 0 (in order they were defined)
layout (std140, set = 3, binding = 0) uniform MaterialUniform {
  vec4 stereoParams;
  vec4 customParams;
} g_MaterialUniform;

vec2 stereo(vec2 uv) {
  return getStereoPassId() * g_MaterialUniform.stereoParams.xy + uv * g_MaterialUniform.stereoParams.zw;
}

void main() {
  App2VertexUnpacked app = getApp2VertexUnpacked();

  vec4 wPos4 = g_PrimitiveUniform.worldFromObject * vec4(app.position, 1.0f);
  vertexOut.albedoCoord = stereo(app.uv);
  vertexOut.lighting = app.incomingLighting;
  vertexOut.worldPosition = wPos4.xyz;
  vertexOut.worldNormal = normalize((transpose(g_PrimitiveUniform.objectFromWorld) * vec4(app.normal, 0.0f) ).xyz);

  gl_Position = getClipFromWorld() * wPos4;

  postprocessPosition(gl_Position);
}
```

```c
// in data/shaders/custom/360.frag
...

// vec4s are stored in set 3, binding 0 (in order they were defined)
layout (std140, set = 3, binding = 0) uniform MaterialUniform {
  vec4 stereoParams;
  vec4 customParams;
} g_MaterialUniform;

// textures are in set 3, in bindings 1+ (in order they were defined)
layout (set = 3, binding = 1) uniform sampler2D albedoSampler;

...

layout (location = 0) out vec4 outColor;

void main() {

  vec4 pixel = texture(albedoSampler, vertexOut.albedoCoord);

  //direction the transition will start
  vec3 direction = vec3(0.0, 0.0, 1.0);

  //angular distance the vetex is from the direction, from -1 to 1
  float d = dot(vertexOut.worldNormal, direction);
  d = (d+1.0)*0.5; //normalise the dot product to 0 to 1

  float amount = clamp(1.0-g_MaterialUniform.customParams.x, 0.0, 1.0);
  float feather = 0.05;
  float alpha = smoothstep(d-feather, d+feather, amount);

  outColor.rgba = vec4(pixel.rgb, alpha);
}
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-ecs.md
---
title: Entity-Component-System (ECS)
description: The Entity-Component-System (ECS) is a central interface to the Spatial SDK runtime, composed of entities, components, and systems that work together
last_updated: 2024-10-16
---

## Overview

ECS is the central interface to the Spatial SDK runtime. ECS is composed of entities, components, and systems. In Spatial SDK, components and entities constitute the entirety of our data model. Entities are essentially just IDs, represented as long integers, that group your components. Within these entities, a set of APIs allows access to information about the components, but the only data that resides directly on the entity is the long integer itself.

## Components and attributes

Components are reusable data units, a little bit like rows in a traditional SQL table. They hold primitives, called attributes, and each component attached to an entity represents a piece of the data model. Components are declared in the code as structures of attributes.

Entities, components, and attributes form a nested hierarchy, where entities contain groups of components, and components contain lists of attributes.

- Attributes: These are the lowest level of data storage and contain things like integers and maps.
- Components: These reusable data containers hold attributes of various Spatial SDK primitive data types.
- Entities: These are wrappers around components and can represent things.

If you go through Spatial SDK's tutorials, you’ve already encountered several components in previous sections:

- A panel component to showcase the Android UI
- A mesh component to render a cube.
- A transform component to describe the cube's location.

These components hold data and allow you to modify an entity.

Consider the following code:

```kotlin
Entity.create()
```

This code creates an entity. However, this entity won’t perform any actions or display anything in the scene. The entity exists, but is invisible to the user and does not impact the scene’s functionality. To make the entity perform a function, you must give it data. This is where reusable components come into play.

Add data to the entity code above by using a `Mesh` component:

```kotlin
Entity.create(
        Mesh(Uri.parse("baseball_cap.glb")),
    )
```

Behind the scenes, the `Mesh` component stores the URI you passed in. The Spatial SDK codebase defines the `Mesh` component as follows:

```kotlin
class Mesh(
    mesh: Uri = Uri.parse("about:blank"),
    hittable: MeshCollision = MeshCollision.LineTest,
    defaultShaderOverride: String = "",
    defaultSceneOverride: Int = -1,
) : ComponentBase() {

  var meshInternal by StringAttribute(R.string.mesh, this, mesh?.toString())
  var mesh: Uri
    get() {
      return Uri.parse(meshInternal)
    }
    set(value) {
      meshInternal = value.toString()
    }

  var hittable by EnumAttribute(R.string.mesh_hittable, this, MeshCollision::class.java, hittable)

  var defaultShaderOverride by
      StringAttribute(R.string.mesh_default_shader_override, this, defaultShaderOverride)

  override fun typeID(): Int {
    return Mesh.id
  }

  companion object : ComponentCompanion {
    override val id = R.id.mesh_class
    override val createDefaultInstance = { Mesh() }
  }
}
```

This class uses attribute parameters to store and retrieve data from the internal data model. This allows you to store and retrieve the `meshUri` you passed in. However, it doesn't provide functionality. To see how adding a `Mesh` component to the entity causes the system to display the entity as a 3D model in the scene, you need to understand systems.

When you are finished with an `Entity`, regardless of the type (`Panel`, `Mesh`, or anything else), you can use the following code:

```kotlin
myEnt.destroy()
```

Spatial SDK's systems will clean up your destroyed entities.

## Systems

Components assign data to an entity, but they don’t provide functionality. To add functionality, we need to connect systems to our entities.

Spatial SDK has a rendering system that checks every entity in the scene. If an Entity has a `Mesh` component attached, the SDK retrieves the file at the `meshUri` and renders it in the scene. The rendering system is large, but this pseudo-code demonstrates how it works:

```kotlin
class RenderingSystem(): System {
  // Systems are run by calling the execute function
  override fun execute() {
    // Get every Entity with a Mesh Component
    Query.where{ has(Mesh.id) }.forEach { entity ->
      val mesh = entity.getComponent<Mesh>()
      val meshUri = mesh.meshUri
      scene.renderGLTF(meshUri)
    }
  }
}
```

Systems are the encapsulation of on-tick functionality for Spatial SDK. For example, you can extend the code above to check if the entity has a `Transform` component attached. If so, Spatial SDK will adjust the location where it renders the model based on the data stored in the `Transform` component.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-editor.md
---
title: Connecting Spatial Editor
description: Meta Spatial SDK uses glXF for scene layout and composition.
last_updated: 2025-02-19
---

## Use the Spatial SDK Gradle Plugin

The best way to connect your app is to use the Spatial SDK Plugin. It registers gradle tasks that assist you with connecting your Spatial Editor Project to your Spatial SDK app. This page covers the export and `generateComponents` tasks.

### Apply the plugin

Apply the Spatial SDK Plugin in your app level `build.gradle.kts` like so:

``` kotlin
plugins {
    ...
    id("com.meta.spatial.plugin")
}
```

### Using the export task

The export task uses the Spatial Editor CLI to export your Spatial Editor Project to a glXF format that is usable by your Spatial SDK app. The first thing you need to do is add information to your app level `build.gradle.kts` that details what you want to export and where. We can export the entire project or individual compositions and objects. We want to define the `metaspatial` file we want to export and where in the `assets` directory we want to export it.

There is also the ability to set the path to the Spatial Editor CLI. If not provided, the export task will use a default value for the app's location.

#### Setting Up Exports
Here's an example of what you could add to export:

``` kotlin
val projectDir = layout.projectDirectory
val sceneDirectory = projectDir.dir("scenes")
spatial {
  scenes {
    // if you have installed Meta Spatial Editor somewhere else, update the file path.
    // cliPath.set("/Applications/Meta Spatial Editor.app/Contents/MacOS/CLI")
    exportItems {
        // This item exports your entire project
        item {
            projectPath.set(sceneDirectory.file("Main.metaspatial"))
            outputPath.set(projectDir.dir("src/main/assets/scenes"))
        }
        // This item only exports the given composition and it's contained compositions
        // and objects
        item {
            projectPath.set(sceneDirectory.file("Main.metaspatial"))
            outputPath.set(projectDir.dir("src/main/assets/composition/comp"))
            compositionPath.set(sceneDirectory.file("Comp1/Main.metaspatialcomp"))
        }
        // This item only exports the given object
        item {
            projectPath.set(sceneDirectory.file("Main.metaspatial"))
            outputPath.set(projectDir.dir("src/main/assets/obj1"))
            cosmoObjectPath.set(sceneDirectory.file("duck/Main.metaspatialobj"))
        }
    }
  }
}
```

#### Running the export task

Now that we have the export task set up, we can run it like any gradle task.


![export gradle task](/images/fa_aether_spatialeditor_exporttask.png)

You can make the export task run automatically by adding this to your app level `build.gradle.kts`.

``` kotlin
afterEvaluate {
    tasks.named("assembleDebug") {
        dependsOn("export")
    }
}
```

You can replace `assembleDebug` with whichever task you're using to build your app. This will make it so that the export task runs anytime you build your app, and you won't need to worry about exporting anymore

### Using Components In Spatial Editor

The Spatial Editor includes built-in components from the Spatial SDK toolkit. However, if you need additional components, such as Physics or custom ones, you can define them using either XML or Kotlin.

### Define components in XML

Add a component [XML](/documentation/spatial-sdk/spatial-sdk-component#creating-a-new-component) file in `app/src/main/components`. The Spatial Editor will read the XML defined in the folder and display your custom components in UI. If you prefer to use another directory, refer to [Specify the custom components folder](/documentation/spatial-sdk/spatial-sdk-component#specify-the-custom-components-folder).

### Define components in Kotlin (deprecated)

Although XML is the recommended way for defining components as of SDK v0.5.5, you can still use Kotlin. To do so, run the `generateComponents` task. The `generateComponents` task will generate a JSON file with information about the components in your app. This JSON should be placed next to your main `metaspatial` file.

**Note**: Certain attributes such as `Entity` and `ExperimentalMap` are not currently supported in the Spatial Editor.

Start by setting up the config needed to run the `generateComponents` task.

#### Set up custom components with Kotlin Symbol Processing (KSP)

Add the KSP plugin to our app:

``` kotlin
plugins {
    ...
    id("com.meta.spatial.plugin") version "0.6.0" apply true
    id("com.google.devtools.ksp") version "1.9.25-1.0.20"
}
```

Next, add the plugin as a KSP dependency to our app. This allows us to add your custom components to the components.json.

``` kotlin
dependencies {
    ...
    ksp("com.google.code.gson:gson:2.11.0")
    ksp("com.meta.spatial.plugin:com.meta.spatial.plugin.gradle.plugin:0.6.0")
}
```

You can find your `custom_components.json` in your `app/build/generated/ksp`. The exact subdirectory will depend on what build task you are using.

![add custom LookAt Component](/images/fa_aether_spatialeditor_customcomponentsjson.png)

#### Set Up generateComponents task

Next we need to set up the config. We need to define where our Spatial Editor project is and where our custom components are stored. Here's an example:

``` kotlin
val projectDir = layout.projectDirectory
val sceneDirectory = projectDir.dir("scenes")
spatial {
    allowUsageDataCollection.set(true)
    scenes {
        componentGeneration {
            outputPath.set(sceneDirectory)
            // We attempt to auto-detect where your "custom_components.json" is placed but if this does
            // not work then you can uncomment the following line and force it to a specific location.
            // customComponentsPath.set(projectDir.dir("build/generated/ksp/debug/resources"))
        }
    }
}
```

#### Running the generateComponents task

Now that we have the generateComponents task set up, we can run it like any gradle task.


![generateComponents gradle task](/images/fa_aether_spatialeditor_generatecomponentstask.png)

You can make the generateComponents task run automatically after your build by adding this to your app level `build.gradle.kts`.

``` kotlin
afterEvaluate {
    tasks.named("assembleDebug") {
        finalizedBy("generateComponents")
    }
}
```

You can replace `assembleDebug` with whichever task you're using to build your app. This will make it so that the generateComponents task runs anytime you build your app.

### Using components in Spatial Editor
Now open your Spatial Editor Project in Spatial Editor. Select the object you want to add the component to. Then when you add a component, all of the components available in your app will be available to add.

![add custom LookAt Component](/images/fa_aether_spatialeditor_addcustomcomponent.png)

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-environment.md
---
title: Create an environment
description: Meta Spatial SDK offers multiple options to customize your app's environment to achieve your desired look and feel.
last_updated: 2024-11-25
---

## Overview

Spatial SDK offers multiple options to customize your app's environment to achieve your desired look and feel. By configuring skyboxes, you can define the backdrop of your virtual world with expansive images, while image-based lighting can cast plausible real-world light and reflections on objects within your scene. This page will guide you through the steps to configure both features, ensuring your application not only performs well but also looks good.

## Skybox

A skybox is the background of a Meta Spatial app. Without a skybox, the background of an app would appear black and empty.

### Creating a skybox mesh

A skybox is essentially a large, spherical mesh with a texture on it. You can create a skybox just like you create a regular mesh:

```kotlin
Entity.create(
        listOf(
            Mesh(Uri.parse("mesh://skybox")),
            Material().apply {
              baseTextureAndroidResourceId = R.drawable.skydome
              unlit = true
            },
        ))
```

### Applying a skybox material

You can customize the skybox by applying different materials. The materials can be a solid color or an image.

- Using a solid color

    Here's an example of applying a yellow color to the skybox with the following RGBA values: `rgba(1.0f, 1.0f, 0, 1.0f)`. Each float value ranges from 0 to 1.

    ```kotlin
    import com.meta.spatial.core.Color4

    Entity.create(
        listOf(
            Mesh(Uri.parse("mesh://skybox")),
            Material().apply {
                baseColor = Color4(1.0f, 1.0f, 0.0f, 1.0f)
            })
    ```


- Using an image

    The skybox material can also be an [equirectangular](https://en.wikipedia.org/wiki/Equirectangular_projection) image. You can apply a material with the image texture like this:

    ```kotlin
    Entity.create(
            listOf(
                Mesh(Uri.parse("mesh://skybox")),
                Material().apply {
                    baseTextureAndroidResourceId = R.drawable.skydome
                    unlit = true
                },
            ))
    ```

    `R.drawable.skydome` refers to the local file of `res/drawable/skydome.jpg`, and `unlit = true` prevents scene lighting from affecting the skybox

## Image-based lighting

Image-based Lighting (IBL) is an efficient method for achieving realistic lighting conditions  without the need to manually configure the lighting environment.

![Comparison with and without IBL](/images/fa_aether_lighting.png)

### Enabling IBL

Follow these steps to enable IBL:

1. Obtain an HDR file. Various sources provide these files, but [PolyHaven](https://polyhaven.com/hdris) is a recommended source and free for commercial use. In the download options, select **4K HDR**.
2. Convert the HDR file to an `.env` file using the [Babylon js texture tool](https://www.babylonjs.com/tools/ibl/). Drag and drop your file into the tool, and it will generate an `.env` file for download.
3. Add the `.env` file to your app assets in the `/<appname>/assets/` folder.
4. Enable the `.env` file in your app by adding the following code to your main activity's `onSceneReady()` method:

    ```kotlin
    scene.updateIBLEnvironment("filename.env")
    ```

5. _Optional_: Turn off your ambient light source in your scene, as IBL generally provides ample ambient light.

    ```kotlin
    scene.setLightingEnvironment(
        Vector3(0.0f, 0.0f, 0.0f),  // ambient light color (none in this case)
        Vector3(0.6f, 0.6f, 0.3f),  // directional light color
        -Vector3(1.0f, 3.0f, 2.0f), // directional light direction
    )
    ```

6. _Optional_: Ensure your skybox is unlit. Otherwise, it may look strange.
7. _Optional_: You can adjust the intensity of your IBL using the environment intensity multiplier:

    ```kotlin
    scene.setLightingEnvironment(
        Vector3(...),
        Vector3(...),
        Vector3(...),
        0.8f // lower number means darker, default is 1.0f
    )
    ```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-events.md
---
title: Event system
description: Introduction to events
last_updated: 2024-10-16
---

## Overview

The event system is an integral part of Spatial SDK applications. It is built into the [DataModel](/documentation/spatial-sdk/spatial-sdk-architecture/#datamodel) class and is designed to handle various types of events that can occur within a Spatial SDK app.

### Event definition

Spatial SDK applications support various types of events. You can define an event by subclassing the `EventArgs` class:

```kotlin
open class EventArgs(
    val eventName: String,
    val dataModel: DataModel,
    var handled: Boolean = false,
    var throttleTime: Int? = null
) {}
```

Here are explanations for the properties:
- `eventName`: the name of the event.
- `dataModel`: the dataModel object of the application.
- `handled`: a boolean to indicate whether the event is handled.
- `throttleTime`: an optional time in milliseconds to throttle the event.

The following defines `PhysicsCollisionCallbackEventArgs`, subclass of the `EventArgs` class:

```kotlin
class PhysicsCollisionCallbackEventArgs(
    val collidedEntity: Entity,
    val collisionPosition: Vector3,
    val collisionNormal: Vector3,
    val impulse: Float,
    datamodel: DataModel,
) : EventArgs(eventName = PhysicsCollisionCallbackEventArgs.EVENT_NAME, dataModel = datamodel) {
  companion object {
    val EVENT_NAME = "physicscollision"
  }
}
```

The name of the event above is `physicscollision`.

### Event registration

Events are tied to entities. To register an event for an entity, invoke its `registerEventListener` method:

```kotlin
Entity.create(...)
      .registerEventListener()<PhysicsCollisionCallbackEventArgs>(
              PhysicsCollisionCallbackEventArgs.EVENT_NAME) { Entity, eventArgs ->
                eventArgs.throttleTime = 200
              }
```

This code registers an event listener for the `physicscollision` event on the specified entity and defines the callback function to execute. When the event occurs, the listener will be notified and can perform the necessary actions.

### Sending the event

Once an event is defined and registered, you can send it from anywhere in the app.

The following code sends a `physicscollision` event. Under the hood, the `DataModel` will retrieve the corresponding listener in the listener registry to handle the event.

```kotlin
val dm = EntityContext.getDataModel()!!
dm.sendEvent(
    Entity(collider),
    PhysicsCollisionCallbackEventArgs.EVENT_NAME,
    PhysicsCollisionCallbackEventArgs(Entity(collided), collisionPos, normal, impulse, dm),
)
```

### Throttling control

You can throttle an event a certain amount of time after the first event that type is sent.

In this example, the `DataModel` will remove the listener for `physicscollision` 200 milliseconds after the first `physicscollision` event is sent. After that, sending `physicscollision` will no longer trigger the event callback.

```kotlin
Entity.create(...)
      .registerEventListener()<PhysicsCollisionCallbackEventArgs>(
              PhysicsCollisionCallbackEventArgs.EVENT_NAME) { Entity, eventArgs ->
                eventArgs.throttleTime = 200
              }
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-explainer.md
---
title: Spatial SDK overview
description: Spatial SDK is a new way to build immersive apps for Meta Horizon OS.
engine: spatial-sdk
last_updated: 2024-03-25
---

Spatial SDK is a new way to build immersive apps for Meta Horizon OS. Spatial SDK lets you combine the rich ecosystem of Android development and the unique capabilities of Meta Quest via accessible APIs. It is Kotlin based, allowing you to use the mobile development languages, tools, and libraries you’re already familiar with. You can build completely new immersive apps, or take your existing mobile app and extend it by adding spatial features.

## Why use Spatial SDK?

- **Easy to get started**: Spatial SDK looks and feels very familiar to mobile developers, enabling you to quickly start building spatial experiences
- **Simple to learn**: Spatial SDK simplifies HorizonOS development with intuitive APIs, so developers can easily integrate key platform capabilities into their experiences
- **Fast to build**: The Spatial SDK workflow is fast so you can iterate quickly on your app. Our developer tools and capabilities let you quickly build and test your ideas.
- **Additive to mobile**: Spatial SDK allows developers to build on top of their existing engineering stack and infrastructure while leveraging the wide ecosystem of libraries and tools available to mobile devs

## Spatial SDK capabilities

- **Mixed reality**: Spatial SDK supports key mixed reality features such as passthrough, scene, anchors and Mixed Reality Utility Kit (MRUK); enabling devs to quickly build apps that blend the virtual and physical world.
- **Realistic 3D graphics**: Spatial SDK supports modern graphics pipelines including GLTF, physically-based rendering (PBR), image-based lighting, skeletal animations, and rigid body physics, so that developers can create compelling 3D experiences
- **Complete scene composition**: Spatial SDK supports complex compositions containing 3D assets, animations, sounds, physics and more. Build full scenes with Spatial Editor or create them at runtime using code.
- **Interactive panels**: Spatial SDK supports rich panels within your scene built using your preferred 2D UI framework.

## Get started

Start developing with Spatial SDK by [Building your first app](/documentation/spatial-sdk/spatial-editor-create-app-content/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-filters.md
---
title: Filters
description: A Meta Spatial SDK tutorial on Filters
last_updated: 2025-04-22
---

## Overview

[Queries](/documentation/spatial-sdk/spatial-sdk-queries) are used to find entities which have a specific set of components or have components that have changed since the last tick. However, you may want to further filter the results of a query to only include entities that match certain criteria. For example, you may want to only include entities whose attributes are equal to some specific values. This is where filters come in.

## Attribute data

To write a filter, you need to access the attribute data of an entity. An entity's attribute data is stored in its components. The Spatial SDK build process generates an attribute data property for each attribute of each component. The name of the attribute data property is always the name of the attribute with the suffix "Data". For example, the `min` attribute of `Box` has the attribute data `minData`.

## Write a filter

Spatial SDK provides a set of filter functions that can be used to filter entities based on their attribute data.

### Logical operators

There are three logical operators in a filter: `and`, `or`, and `not`.

- The `and` operator is used to "and" the two conditions on either side.
- The `or` operator is used to "or" the two conditions on either side.
- The `not` operator is used to negate the condition within the parentheses.

```kotlin
// Filters entities that are local and whose "type" attribute is equal to "eye_gaze" or "head"
val entities = Query.where { changed(AvatarAttachment.id) }
        .filter { isLocal() and (by(AvatarAttachment.typeData).isEqualTo("eye_gaze") or by(AvatarAttachment.typeData).isEqualTo("head")) }
        .eval()
```

For example, the code above shows how to use the `and` and `or` operators to filter entities based on the type attribute data of the `AvatarAttachment` component. You can use parentheses to group conditions together.

### IntAttribute, FloatAttribute, LongAttribute, TimeAttribute

The code below shows how to use `IntAttribute` to filter entities based on the data of the attribute `intAttr`.

```kotlin
// Filters entities where intAttr is equal to 1
val ents0 = Query.where { has(TestComponent.id) }
              .filter { by(TestComponent.intAttrData).isEqualTo(1) }
              .eval()

// Filters entities where intAttr is greater than 1
val ents1 = Query.where { has(TestComponent.id) }
            .filter { by(TestComponent.intAttrData).greaterThan(1) }
            .eval()

// Filters entities where intAttr is greater than or equal to 1
val ents2 = Query.where { has(TestComponent.id) }
            .filter { by(TestComponent.intAttrData).greaterThanOrEqualTo(1) }
            .eval()

// Filters entities where intAttr is less than 1
val ents3 = Query.where { has(TestComponent.id) }
            .filter { by(TestComponent.intAttrData).lessThan(1) }
            .eval()

// Filters entities where intAttr is less than or equal to 1
val ents4 = Query.where { has(TestComponent.id) }
            .filter { by(TestComponent.intAttrData).lessThanOrEqualTo(1) }
            .eval()
```

`FloatAttribute`, `LongAttribute`, and `TimeAttribute` have identical APIs to those of `IntAttribute`.

### BooleanAttribute

The code below shows how to use `BooleanAttribute` to filter entities based on the data of the attribute `boolAttr`.

```kotlin
 // Filters entities where boolAttr is equal to true
val ents0 = Query.where { has(TestComponent.id) }
              .filter { by(TestComponent.boolAttrData).isEqualTo(true) }
              .eval()
```

### StringAttribute

The code below shows how to use `StringAttribute` to filter entities based on the data of the attribute `stringAttr`.

```kotlin
// Filters entities where stringAttr is equal to "hello"
val ents0 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.stringAttrData).isEqualTo("hello") }
    .eval()

// Filters entities where stringAttr is equal to "Hello" case-insensitively
val ents1 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.stringAttrData).isEqualToCaseInsensitive("Hello") }
    .eval()

// Filters entities where stringAttr contains "ell"
val ents2 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.stringAttrData).contains("ell") }
    .eval()

// Filters entities where stringAttr starts with "he"
val ents3 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.stringAttrData).startsWith("he") }
    .eval()

// Filters entities where stringAttr ends with "lo"
val ents4 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.stringAttrData).endsWith("lo") }
    .eval()

// Filters entities where stringAttr is greater than "hello"
val ents5 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.stringAttrData).greaterThan("hello") }
    .eval()

// Filters entities where stringAttr is less than "hello"
val ents6 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.stringAttrData).lessThan("hello") }
    .eval()

// Filters entities where stringAttr is greater than or equal to "hello"
val ents7 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.stringAttrData).greaterThanOrEqualTo("hello") }
    .eval()
```

### EnumAttribute

The code below shows how to use `EnumAttribute` to filter entities based on the data of the attribute `enumAttr`.

```kotlin
// Filters entities where enumAttr is equal to MyEnum.VALUE1
val filteredEntities = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.enumAttrData).isEqualTo(MyEnum.VALUE1) }
    .eval()
```

### Vector2Attribute, Vector3Attribute, Vector4Attribute

The code below shows how to use `Vector4Attribute` to filter entities based on the data of the attribute `vector4Attr`.

```kotlin
// Filters entities where vector4Attr is equal to Vector4(1.0f, 2.0f, 3.0f, 4.0f)
val ents0 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.vector4AttrData).isEqualTo(Vector4(1.0f, 2.0f, 3.0f, 4.0f)) }
    .eval()

// Filters entities where vector4Attr's x property is greater than 1.0f
val ents1 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.vector4AttrData).byX().greaterThan(1.0f) }
    .eval()

// Filters entities where vector4Attr's y property is less than 2.0f
val ents2 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.vector4AttrData).byY().lessThan(2.0f) }
    .eval()

// Filters entities where vector4Attr's z property is greater than or equal to 3.0f
val ents3 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.vector4AttrData).byZ().greaterThanOrEqualTo(3.0f) }
    .eval()

// Filters entities where vector4Attr's w property is less than or equal to 4.0f
val ents4 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.vector4AttrData).byW().lessThanOrEqualTo(4.0f) }
    .eval()
```

`Vector2Attribute` and `Vector3Attribute` have similar APIs to those of `Vector4Attribute`.

### PoseAttribute

The code below shows how to use `PoseAttribute` to filter entities based on the data of the attribute `poseAttr`.

```kotlin
// Filters entities where poseAttr is equal to Pose(Vector3(1.0f, 2.0f, 3.0f), Quaternion(4.0f, 5.0f, 6.0f, 7.0f))
val ents0 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.poseAttrData).isEqualTo(Pose(Vector3(1.0f, 2.0f, 3.0f), Quaternion(4.0f, 5.0f, 6.0f, 7.0f))) }
    .eval()

// Filters entities where poseAttr's position x property is greater than 1.0f
val ents1 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.poseAttrData).byPositionX().greaterThan(1.0f) }
    .eval()

// Filters entities where poseAttr's position y property is less than 2.0f
val ents2 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.poseAttrData).byPositionY().lessThan(2.0f) }
    .eval()

// Filters entities where poseAttr's position z property is greater than or equal to 3.0f
val ents3 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.poseAttrData).byPositionZ().greaterThanOrEqualTo(3.0f) }
    .eval()

// Filters entities where poseAttr's orientation w property is less than or equal to 4.0f
val ents4 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.poseAttrData).byOrientationW().lessThanOrEqualTo(4.0f) }
    .eval()

// Filters entities where poseAttr's orientation x property is greater than 5.0f
val ents5 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.poseAttrData).byOrientationX().greaterThan(5.0f) }
    .eval()

// Filters entities where poseAttr's orientation y property is less than 6.0f
val ents6 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.poseAttrData).byOrientationY().lessThan(6.0f) }
    .eval()

// Filters entities where poseAttr's orientation z property is greater than or equal to 7.0f
val ents7 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.poseAttrData).byOrientationZ().greaterThanOrEqualTo(7.0f) }
    .eval()
```

### UUIDAttribute

The code below shows how to use `UUIDAttribute` to filter entities based on the data of the attribute `uuidAttr`.

```kotlin
// Filters entities where uuidAttr is equal to UUID.fromString("123e4567-e89b-12d3-a456-426614174000")
val ents0 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.uuidAttrData).isEqualTo(UUID.fromString("123e4567-e89b-12d3-a456-426614174000")) }
    .eval()
```

### EntityAttribute

The code below shows how to use `EntityAttribute` to filter entities based on the data of the attribute `entityAttr`.

```kotlin
// Filters entities where entityAttr's entity id is equal to that of entity1

val entity1 = Entity.create() // entity1 is an Entity object
val ents0 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.entityAttrData).isEqualTo(entity1) }
    .eval()
```

### ExperimentalMapAttribute

The code below shows how to use `ExperimentalMapAttribute` to filter entities based on the data of the attribute `mapAttr`.

```kotlin
// Filters entities where mapAttr contains the key "key1"
val ents0 = Query.where { has(TestComponent.id) }
    .filter { by(TestComponent.mapAttrData).containsKey("key1") }
    .eval()
```

### IsLocal

The code below shows how to use `IsLocal` to filter entities based on whether they are local or not.

```kotlin
// Filters entities that are local
val ents0 = Query.where { has(TestComponent.id) }
    .filter { isLocal() }
    .eval()
```

## Kotlin Filters vs Native Filters

The two queries below will return the same results, but the first uses a Kotlin filter and the second uses a native filter.

```kotlin
val droneEntities0 =
    Query.where { has(DroneComponent.id, Transform.id) }
        .eval()
        .filter { it.getComponent<DroneComponent>().enabled == true }

val droneEntities1 =
    Query.where { has(DroneComponent.id, Transform.id) }
        .filter { by(DroneComponent.enabledData).isEqualTo(true) }
        .eval()
```

For a query with thousands of entities, using a native filter can be 100 times more efficient than using a Kotlin filter. This is because `it.getComponent<DroneComponent>()` is a function that creates a new `DroneComponent` object for each entity, and object creation in large numbers is slow in Kotlin. Meanwhile, `by(DroneComponent.enabledData)` is an API that directly accesses the data of the `DroneComponent` on the C++ side, and is much faster than creating a new `DroneComponent` object.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-gltfs.md
---
title: glTFs
description: Meta Spatial SDK uses glTF (GL Transmission Format) for loading custom 3D models. It is a standard file format for delivering 3D graphics efficiently.
last_updated: 2024-11-11
---

## Overview

Spatial SDK uses glTF (GL Transmission Format) for loading custom 3D models. It is a standard file format for delivering 3D graphics efficiently. You can think of it as as "JPEG of 3D". A `.glb` file is the binary version of the `.gltf` file, which includes textures, geometry, and other assets in a single file, making it convenient for distribution.

## Anatomy of a glTF file

In the context of Spatial SDK, you need to know the following:

- A glTF file has a scene with a hierarchy of nodes.
- Each node can have a transform (translate, rotation, scale) and a mesh.
- Each mesh points to some geometry data (vertices and indices) and a material.
- Each material specifies some PBR (Physically Based Rendering) properties (roughness/metallicness) and may point to a texture.

## Supported formats

The following extensions are supported:

- `KHR_texture_transform`
- `KHR_texture_basisu`
- `KHR_materials_unlit`
- Approximate support for `KHR_materials_pbrSpecularGlossiness`, for displaying some legacy materials.

## Sourcing glTF/glb models

**Online:** There are many options for finding glTFs online. [Sketchfab](https://sketchfab.com) is a popular platform for free and paid high-quality glTF and `.glb` models. Search for the model you need and download it in `.glb` format.

**Create Your Own:** If you want to create custom 3D models, software like Blender allows you to design and export your creations in the glTF or `.glb` format. You can also edit the files you find online and then export them to the `.glb` for Spatial SDK (even ones in other file formats).

## Loading your `.glb`s in Spatial SDK

As described in the [3D Objects page](/documentation/spatial-sdk/spatial-sdk-3dobjects/), once you've downloaded your asset (say `mymodel.glb`), copy it to the assets folder of your app (`<myapp>/assets/`). You can now load it into your app by using the `Mesh` component:

```
Entity.create(
    listOf(
        Mesh(
          Uri.parse("mymodel.glb")
        )
    )
)
```

## Tools for working with glTF files

This section contains a list of tools to work with glTF files.

### Blender

[Blender](https://www.blender.org/) is a free and open-source 3D creation tool. Although it can be intimidating for beginners, there are lots of high-quality, free learning resources across the Internet.

#### Importing Models

Blender supports importing from many different 3D model types (for example, `.obj`, `.fbx`, `.dae`). You can often import any supported model type and export it to glTF inside Blender.

You can get models and animations from [Mixamo](https://www.mixamo.com/), which provides free and realistic character animations. Using models from Mixamo, you can put your character into a walk cycle or have them do a backflip, without worrying about rigging or hand animating the model yourself. However, Mixamo doesn’t support exporting to glTF. Instead, you can download the animation as an `.fbx`, import it into Blender, and then export it to glTF.

#### Exporting as glTF

Blender has a page on its [full glTF support](https://docs.blender.org/manual/en/2.80/addons/io_scene_gltf2.html). You can export by clickign on **File** > **Export** > **glTF 2.0 (.glb/.gltf)**. Exporting as a `.glb` file is the best option, as it is a bit easier to move between programs.

After you export, try using a glTF standard model viewer to check if you exported the model correctly. It is best to ensure your models look correct in a commonly used viewer.

If your materials do not show up correctly in a standard viewer, make sure you are using the Principled BSDF shader node for them in Blender. Blender uses this shader to know how to export your material properties.

### Khronos resources

Khronos, the organization behind the glTF standard, offers several tools and assets for working with glTF files.

#### Sample models

The community has curated a set of [sample glTF/glb files](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0) for testing and verifying the correctness of different glTF features. Some of these models are used in our sample apps.

#### Sample Viewer

Khronos’ [glTF Sample Viewer](https://github.khronos.org/glTF-Sample-Viewer-Release/) is a reference implementation of a glTF viewer. You can access all the sample models mentioned in the previous section and drag and drop them into any custom models.

### VS Code Plugin

![Screenshot of the VS Code glTF plugin](/images/spatial_sdk_gltf_vs_code.png)

CesiumJS has made a useful [VS Code plugin](https://marketplace.visualstudio.com/items?itemName=cesium.gltf-vscode) for working with glTF files. With this plugin, you can inspect your glTF files with rich code navigation, use a built-in model viewer with multiple reference implementations (CesiumJS, Three.js, and Babylon.js), and debug your models with a hierarchy explorer. The plugin's information page gives a helpful overview of how to use it.

### glTF Transform

[glTF Transform](https://gltf-transform.dev/) is a powerful JS library that processes glTF files. It enables you to read, modify, prune, optimize, and customize your glTF models.

You can use glTF Transform to convert your assets to the correct format for Spatial SDK. For example, the assets from [Flowerbed](https://flowerbed.metademolab.com/) are glTFs that include data for collision boxes and boundaries of the environment. Flowerbed has a custom glTF processor to strip out and process the collision data when loading the asset. In Spatial SDK, you might want to display these models without caring about the collision data. You can use a script to strip out all the collision data before giving the files to Spatial SDK:

```
function customTransform(options) {
  return async document => {
    for (const nodes of document.getRoot().listNodes()) {
      // remove any node marked as a collider or boundary
      // these are not meant to be visible in the actual game
      if (nodes.getExtras().collider == 1 || nodes.getExtras().boundary == 1) {
        nodes.dispose();
        continue;
      }
      // remove any nodes with ".gltf" in the name, used to reference other files
      if (nodes.getName().indexOf('.gltf') != -1) {
        nodes.dispose();
        continue;
      }
    }
  };
}
```

If you don’t want to run these scripts locally, check out the gltf.report tool below.

### gltf.report

![Screenshot of the gltf.report tool](images/spatial_sdk_gltf_report.png)

[gltf.report](https://gltf.report/) is a useful online tool for investigating and profiling your models. One of its most valuable features is the integration with glTF transform, which allows you to run your code on your imported model.

Their default glTF transform script can reduce the size of models by pruning the file and resizing textures to a more appropriate size for mobile. This is a good option for reducing the size of your assets in your app.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-glxf.md
---
title: glXF
description: Meta Spatial SDK uses glXF for scene layout and composition.
last_updated: 2024-11-11
---

## Overview

[glXF](https://github.com/KhronosGroup/glTF-External-Reference/blob/main/specification/2.0/README.md) (or glTFx) is a file format that enables the composition of glTFs and other glXFs. Spatial SDK uses glXF for scene composition and layout purposes.

Spatial Editor exports the glXF format, which you can inflate into an Spatial SDK app. Spatial SDK apps utilize the GLXFManager to manage glXF inflation, deletion, and queries.

## Loading and inflating a glXF

Loading and inflating a glXF means loading the file and inflating the nodes as Spatial SDK entities. These entities will have the proper `Transform` and `Mesh` components, set to correspond to their transform and asset in the glXF.

To load a glXF, launch a coroutine and call glXFManager’s `inflateGLXF` method from your Spatial SDK activity.

```
val myEntity = Entity.create()

private fun loadGLXF() {
  activityScope.launch {
    glXFManager.inflateGLXF(
        Uri.parse("apk:///demoproject1.glxf"),
        rootEntity = myEntity,
        keyName = "example_key_name")
  }
}
```

`inflateGLXF` returns a `GLXFInfo` object, which contains helpful information about the inflated glXF.

`inflateGLXF` takes the following parameters:

- `uri`: The path to the glXF file.
- `rootEntity`:  An optional parameter that sets any entity you want as the `rootEntity` of the glXF. If you don't include this parameter, the `rootEntity` will be a new entity. This parameter is helpful when moving the entire glXF scene altogether. Changing this `rootEntity`'s transform will cause all the inflated entities to move with it.
- `keyName`: An optional parameter that tells GLXFManager to save the GLXFInfo inflated by this glXF using the name you passed into the method. Once saved, you can access this data anytime using the `keyName` you created.

You can load glXFs from the same file as many times as you want.

## Querying glXFs

You can query GLXFInfo using the `keyName` parameter. Two options exist to do this with glXFManager, and both return the GLXFInfo if it exists.

- `glXFManager.getGLXFInfo("example_key_name")`: This method does not check if the GLXFInfo exists, and will throw an error if there is no GLXFInfo for the corresponding key name.
- `glXfManager.tryGetGLXFInfo("example_key_name")`: This method will return null if there is no GLXFInfo for the corresponding key name.

## Querying the nodes and entities of a glXF

A node must have a unique name for it to be queryable in a glXF. Using this name, you can get the GLXFNode and then the inflated entity that represents that node.

```
val glXFInfo = glXFManager.getGLXFInfo("example_key_name")
val myDuckNode: GLXFNode = glXFInfo.getNodeByName("myDuck") // gets GLXFNode
val myDuckEntity = myDuckNode.entity
// Do something with myDuckEntity
```

Similar to querying GLXFInfo, there are two options for querying glXF:

- `getNodeByName`: This call throws an exception if a node with the specified name doesn’t exist.
- `tryGetNodeByName`: This call will return null if the node name doesn’t exist.

You can also pass Android resource string IDs to these functions.

```
val myDuckNode: GLXFNode = glXFInfo.getNodeByName(R.string.my_duck) // gets GLXFNode
```

## Query nested glXFs

You can query nested GLXFInfos by using the `getNestedGLXFInfo` method of GLXFManager.

```
val childGLXFInfo = glXFManager.getNestedGLXFInfo(parentInfo = myGLXFInfo, childName = "myNestedGLXFNodeName")
```

To get GLXFInfo that is nested on more than one level, you can pass in a list of names instead. Treat the list like a file path, where the first name is the first nested GLXF, and so on.

```
val greatGrandChildGLXFInfo = glXFManager.getNestedGLXFInfo(parentInfo = myGLXFInfo, childNamePathList = listOf("child", "grandChild", "greatGrandChild"))
```

## Delete glXFs or entities from glXFs

To delete glXFs, simply destroy the `rootEntity` of the glXF as you would any normal entity.

```
myGLXFInfo.rootEntity.destroy()
```

This call will delete all entities inflated from that glXF and remove its info from the GLXFManager.

You can also independently delete subnodes of a scene. Deleting an entity inflated from a glXF will also automatically delete its children, including those from nested glXFs.

```
val myNode: GLXFNode = glXFInfo.getNodeByName("myNode")
val myEntity = myNode.entity
myEntity.destroy()
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-hot-reload.md
---
title: Hot reload with Spatial Editor
description: Learn how to use the hot reload feature to preview and edit your Meta Spatial Editor compositions quickly.
last_updated: 2025-04-07
---

## Overview

This document guides you through setting up and using hot reload to streamline your development workflow.

Without hot reload, headsets do not automatically rebuild your app when changes occur. To view updates, you must manually save your changes in both the Meta Spatial Editor project and the Meta Spatial SDK files and then rebuild and reinstall the project using Android Studio.

With hot reload enabled, you can instantly preview and edit your Meta Spatial Editor compositions in your headset. This reduces time spent on manual rebuilds and installations. Whether you're working on custom components or exploring sample projects, this guide helps you integrate hot reload into your development process for a more seamless experience.

## Prerequisites

Before you can run Meta Spatial Editor projects on a headset, you must [integrate them with Meta Spatial SDK](/documentation/spatial-sdk/spatial-editor-using-with-sdk/). After you have successfully added your Spatial Editor Project to your app, you are ready to use hot reloading.

If you'd rather temporarily modify entities so you can debug your scene, use the [Data Model Inspector](/documentation/spatial-sdk/spatial-editor-data-model-inspector/).

## Samples using hot reload

The CustomComponentsSample of our [Meta-Spatial-SDK-Samples](https://github.com/meta-quest/Meta-Spatial-SDK-Samples) has hot reload added by default. This means you can open the Spatial Editor project in Spatial Editor, run the **hotReload** Gradle task, and watch as your saved changes get loaded to your headset immediately. If you want to use hot reload for the other samples, you will need to add the `HotReloadFeature` to the the sample app yourself by following the instructions below

## Hot reload

This feature automatically updates the build on your headset whenever a file in the **Assets** folder is modified.

To enable hot reload, install the Meta Spatial SDK Plugin and add the appropriate AAR and config options in `build.gradle.kts`:

```
dependencies {
    ...
    implementation("com.meta.spatial:meta-spatial-sdk-hotreload:$metaSpatialSdkVersion")
}

...

spatial {
  ...
  hotReload {
    appPackage.set("com.your.package")
    appMainActivity.set("com.your.package.YourActivity")
    assetsDir.set(File("src/main/assets"))
  }
}
```

Next, in your Meta Spatial SDK app’s Activity, register `HotReloadFeature`:

```
class MyActivity : AppSystemActivity() {
...
override fun registerFeatures(): List<SpatialFeature> {
    return listOf(
        ... // other features here
        HotReloadFeature(this))
  }
...
}
```

## Installing and running a Meta Spatial application with hot reload

The Meta Spatial Gradle plugin has a built-in Gradle task called `hotReload`. It allows you to install and run your Meta Spatial application while listening to your local file changes.

Click on the **Sync Project with Gradle Files** button in the top right section of Android Studio to make sure the `hotReload` Gradle task is synced.

![Sync Gradle files](/images/fa_aether_hotreload_syncGradle.png)

Make sure you have **Configure all Gradle tasks during Gradle Sync** enabled in your Android Studio settings.

![Gradle task](/images/fa_aether_hotreload_config_GradleSync.png)

After that, you should be able to find the `hotReload` Gradle task:

![Gradle task](/images/fa_aether_hotreload_gradleTask.png)

If you are unable to find it, ensure your task list is rebuilt when you perform a Gradle sync.

To run the `hotReload` Gradle task, select the task and right-click on it, then select `Run 'Sample:app:[hotReload]'`.

![Run Gradle task](/images/fa_aether_hotreload_runGradleTask.png)

Android Studio will install and run the Meta Spatial application. Once the application fully loads in your headset, the Gradle task starts a background process to monitor file changes and hot reload them. If you have the export task set up, all you need to do is save your changes in Spatial Editor. Then it will auto-export the project to your assets folder and initiate the hot reload.

![Gradle task tab](/images/fa_aether_hotreload_runGradleTaskTab.png)

With hot reload enabled, you don't have to re-run the application every time you make a change to a `.glxf`, `.gltf` or `.glb` file. You can also live edit your scene using Meta Spatial Editor, and your scene will in real-time when you save your changes.

## Restrictions

Using the default hot reload mode, the app will delete all entities inflated from your Spatial Editor project and create them again using the reloaded version of your project. If your app has references to entities in the glXF, it will likely crash, as it will try to reference a deleted entity.

## Troubleshooting

Sometimes, the export is not run when you build your app. It will crash and throw an error saying that your glXF file could not be found or parsed. To fix this, you will need to run the export Gradle task manually. You can find it in the same list that you found the `hotReload` task. After you run the export the first time, you should be able to use hot reload normally.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-inputs-controllers.md
---
title: Inputs and controllers
description: Meta Spatial SDK inputs and controllers.
last_updated: 2025-02-11
---

## Overview

Spatial SDK offers seamless integration for using hands and controllers with your Android panel interactions. It forwards the input from your hands or controllers to your Android panels, making it easier to work with inputs.

## The `Controller` component

Use the `Controller` component to interact with input. This component enables you to read data about a single controller instance.

For example:

```kotlin
class Controller(
    var buttonState: Int = 0,
    var changedButtons: Int = 0,
    var isActive: Boolean = false,
    var type: ControllerType = ControllerType.CONTROLLER,
) : Component
```

- `type`: Set this variable to either `ControllerType.CONTROLLER` or `ControllerType.HAND` to specify the type of input you want to use.
- `isActive`: This variable is `true` if a player actively uses the specified input type. For example, if a player uses their hands and the `type` variable is set to `Controller.HAND_TYPE`, `isActive` would be `true`. If players use their controllers, `isActive` would be `false`.
- `buttonState` and `changedButtons`: These variables represent the button states between this tick and the previous one.

## Manage button state

Spatial SDK employs an integer, acting as a bit field, to represent `buttonState` and `changedButtons`. Use a bitwise `and` with the `ButtonBits` enum to extract information from these values.

For hand inputs, `ButtonX` and `ButtonA` represent the left and right index finger pinches, respectively.

```kotlin
// true if the controller is currently pressing the A button
(controller.buttonState and ButtonBits.ButtonA) != 0
// true if the controller is currently holding down either of the triggers
(controller.buttonState and (ButtonBits.ButtonTriggerL or ButtonBits.ButtonTriggerR)) != 0
// a button state representing the buttons that were just pressed down
controller.buttonState and controller.changedButtons
// true if the controller just let go of the X button
(controller.buttonState.inv() and controller.changedButtons and ButtonBits.ButtonX) != 0
```

## Query for controllers

Use the following code to get all entities for the current player with the `Controller` component.

```kotlin
Query.where{ has(Controller.id) }.eval().filter { it.isLocal() }
```

This method has a limitation. It returns a `Controller` component for both hands and controllers, even if only one is active. Use the `AvatarBody` class to work around this limitation. A local entity with an `AvatarBody` component gives you access to the head and active hands controllers.

```kotlin
class AvatarBody(
    var head: Entity,
    var leftHand: Entity,
    var rightHand: Entity,
    var isPlayerControlled: Boolean = false,
) : Component

...

// get the current player's `AvatarBody`
val playerBody : AvatarBody = Query.where{ has(AvatarBody.id) }.eval().filter {
    it.isLocal() &&  it.getComponent<AvatarBody>().isPlayerControlled
}.first().getComponent<AvatarBody>()
// get the left controller that is active
val leftController: Controller = playerBody.leftHand.getComponent<Controller>()
// get the position of the user's head
val headPose: Pose = playerBody.head.getComponent<Transform>().transform
```

## Get the position of the controllers

Entities with a `Controller` component will also have a `Transform` component. You can get the pose with the following code:

```kotlin
val pose: Pose = playerBody.leftHand.getComponent<Transform>().transform
```

## Respond to button presses on meshes

If you want to execute some code in cases where a controller interacts with a mesh, use the `SceneObject.addInputListener()` method. For instance, the following code uses `SceneObject.addInputListener()` to change a sphere’s color when the player points at the sphere and presses the A button:

```kotlin
val red = Color4(1.0f, 0.0f, 0.0f, 1.0f)
val green = Color4(0.0f, 1.0f, 0.0f, 1.0f)
val sphere: Entity = Entity.create(listOf(
    Mesh(Uri.parse("mesh://sphere")),
    Sphere(1.0f),
    Material().apply{ baseColor = red }
))

// later, inside a system
val systemObject =
  systemManager.findSystem<SceneObjectSystem>()?.getSceneObject(entity) ?: return

systemObject.thenAccept{ sceneObject ->
   sceneObject.addInputListener(
    object : InputListener {
        override fun onInput(
            receiver: SceneObject,
            hitInfo: HitInfo,
            sourceOfInput: Entity,
            changed: Int,
            clicked: Int,
            downTime: Long
        ) {
            // check if the A button has changed this tick
            if((changed and ButtonBits.ButtonA) != 0){
                val material = sourceOfInput.getComponent<Material>()
                if((clicked and ButtonBits.ButtonA) != 0) {
                    // set green when first pressing down on the A button
                    material.baseColor = green
                } else {
                    // set red when letting go
                    material.baseColor = red
                }
                sourceOfInput.setComponent(material)
            }
        }
    }
}
```

As an alternative solution, you can attach an event listener directly to the entity without waiting for the mesh to load.

```kotlin
val red = Color4(1.0f, 0.0f, 0.0f, 1.0f)
val green = Color4(0.0f, 1.0f, 0.0f, 1.0f)
val sphere: Entity = Entity.create(listOf(
    Mesh(Uri.parse("mesh://sphere")),
    Sphere(1.0f),
    Material().apply{ baseColor = red }
))
// can attach directly after creating
sphere.registerEventListener<ButtonReleaseEventArgs>(
        ButtonReleaseEventArgs.EVENT_NAME) { entity, eventArgs ->
          if (eventArgs.button == ControllerButton.ButtonA) {
            // make the material green when releasing the A button
            val material = entity.getComponent<Material>()
            material.baseColor = green
            entity.setComponent(material)
          }
        }
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-isdk-grabbable.md
---
title: Grabbables in Interaction SDK
description: Learn about the Interaction SDK's grabbable feature available in Spatial SDK.
last_updated: 2025-04-21
---

Grabbable entities in Spatial SDK can be manipulated by a hand or controller. By default, they can be simultaneously manipulated by only a single device at once. Interaction SDK's grabbable feature adds a new movement type called direct, lets you constrain grabbed objects, and adds two-handed grab support. Interaction SDK's `IsdkToolkitBridgeSystem` automatically adds the grabbable feature to any entity that has both a Spatial SDK `Grabbable` component and either a mesh or collider component, so you don't need to make any manual changes to use the feature. Spatial SDK's default grabbable behavior is also still available.

Interaction SDK's grabbable feature uses the following components:

* IsdkGrabbable
    * Tunes the responsiveness of the grabbed object via smoothing values.
    * Specifies the movement type (Direct, Billboard, or AxialBillboard).

* IsdkGrabbableConstraints
    * Constrains the transforms or scale a grabbed object, and lock the object's position, rotation, and scale attributes. Don't scale entities that have a Physics component.
    * Enables two-handed grab support. When enabling two-handed grab for an object, always apply a min & max scale constraint to prevent the object from becoming too large or small when it's scaled.

## Grabbable object colliders

In order for an object to be detected by the Interaction SDK grab system, it must have a Grabbable component and either a Mesh component or a Collider.

For improved runtime performance and the ability to use touch-grabs (grabbing an object while your hand or controller is inside it), add collider components instead of relying on mesh component collision.

Spatial SDK collision components are mapped to Interaction SDK colliders as follows.

| Spatial SDK Collider | Interaction SDK Collider | Ray Grab | Touch Grab |
|----------------------|--------------------------|----------|------------|
| Box                  | IsdkBoxCollider          | Yes      | Yes        |
| RoundedBox           | IsdkBoxCollider          | Yes      | Yes        |
| Quad                 | IsdkBoxCollider          | Yes      | Yes        |
| Plane                | IsdkBoxCollider          | Yes      | Yes        |
| Sphere               | IsdkSphereCollider       | Yes      | Yes        |
| Mesh                 | n/a                      | Yes      | No         |

## Manually add the Interaction SDK grabbable feature to an entity

If you've disabled Interaction SDK's `IsdkToolkitBridgeSystem` but want to enable advanced grabbing functionality for an entity, follow these steps.

1. Replace the `Grabbable` component on the entity with an `IsdkGrabbable` component.

2. (Optional) Add an `IsdkGrabbableConstraints` component.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-isdk-listen-to-input-events.md
---
title: Listen to input events with ISDK
description: Learn about the input events emitted by the Interaction SDK feature in Spatial SDK.
last_updated: 2025-04-21
---

The `IsdkSystem` emits events through the existing Spatial SDK [InputListener](/reference/spatial-sdk/latest/root/com.meta.spatial.runtime/input-listener) interface. Events are emitted after all grabbed entities have been moved.

When using Interaction SDK in your project, use the `onPointerEvent` method instead of the `onInput` method to get information about interactions. `onPointerEvent` is an alternative, generic way to handle input events. `InputListener.onClickDown`, `onClick`, `onHoverStart`, `onHoverStop` are powered by `onPointerEvent` and so should still be used in place of `InputListener.onInput`.

You should use `onPointerEvent` because it adds the following additional information that's unavailable through regular `InputListener.onInput` style events:

* Accurate Scroll X/Y values as floating point (0 -> 1)
* SemanticType of the interactable - is this a grab, select or scroll (see `SemanticType`)

`onPointerEvent` omits the following information:

* Which controller buttons are pressed

For applications that still rely on the `InputListener.onInput` callback, Interaction SDK Direct Touch interactions, like touching a panel with your fingertip, will be sent as an emulated trigger button press (`ButtonBits.ButtonTriggerL` for left hand/controller or `ButtonBits.ButtonTriggerR` for right hand/controller).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-isdk-overview.md
---
title: Interaction SDK feature overview
description: Learn about the Interaction SDK experimental feature available in Spatial SDK.
last_updated: 2025-04-18
---

Interaction SDK is an experimental feature that is disabled by default. Enabling it replaces the Spatial SDK [InputSystem](/reference/spatial-sdk/latest/root/com.meta.spatial.vr/input-system) with `IsdkSystem`.

With Interaction SDK, you can:
* Use either your hand or controller's ray or pinch interaction to grab 3D meshes or flat panels.
* Interact with panels by touching them directly.
The visible hand or controller will stop from penetrating panels and perform recoil assist to make repeat poking feel more natural.

<section>
  <embed-video width="100%">
    <video-source handle="GAS_UB0X2GR811sCANAkrXKMafQZbosWAAAF" />
  </embed-video>
</section>

<em>Demonstrating grabbing a panel directly and scrolling, and then using the hand's ray interaction to transform an object.</em>

## How the SDK works

Interaction SDK is a native library that is run from within `IsdkSystem`. The native library uses the following components to build a view of entities that can be interacted with, and determine how those entities should respond to interaction.

Panels
* IsdkCurvedPanel
* IsdkPanelDimensions
* IsdkPanelGrabHandle

Grabbing Items
* IsdkGrabbable
* IsdkGrabConstraints
* IsdkBoxCollider
* IsdkSphereCollider

Each app frame, the `IsdkSystem` ticks the native library. This involves:

1. Reading raw input from OpenXR input devices (hands and controllers).
2. Reading Interaction SDK component changes from the ECS data model to add, update, or delete internal 'interactables'.
3. Using physics to determine hit info between input devices and interactables.
4. Resolving any conflicts between interactions (e.g. when multiple interactables are close together, which is grabbed?).
5. Modifying the ECS data model of interactable entities with any positional updates (e.g. grab transforms).
6. Modifying the ECS data model of device visual entities (the hand or controller mesh) to apply touch limiting.
7. Generating a list of PointerEvents and broadcasting to InputListeners (Raw events via onPointerEvent, and
Backwards compatible events via onInput).

## Add Interaction SDK to your project

To enable Interaction SDK in your project, follow these steps.

1. Check that your project is using at least Spatial SDK version 0.6.0.

2. In your main activity class (the one that implements `AppSystemActivity`), add this line at the top of the file.

    ```kotlin
    import com.meta.spatial.isdk.IsdkFeature
    ```

3. In the list returned from `registerFeatures()`, add this line.

    ```kotlin
    IsdkFeature(this, spatial, systemManager),
    ```

    The `registerFeatures()` method should look like this.

    ```kotlin
    override fun registerFeatures(): List<SpatialFeature> {
    val features = mutableListOf<SpatialFeature>(
        VRFeature(this),
        IsdkFeature(this, spatial, systemManager),
    )
    return features
    }
    ```

## Known limitations

* Curved panels cannot be grabbed and transformed.
* By default, panels in Spatial SDK can be grabbed anywhere on the surface using the grip button. When Interaction SDK is enabled, this is not supported - flat panels must be grabbed near their border.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-isdk-panels.md
---
title: Panels in Interaction SDK
description: Learn about the Interaction SDK's panels available in Spatial SDK.
last_updated: 2025-04-21
---

Interaction SDK panels add touch limiting support to an entity, and are best used with a Spatial SDK [PanelSceneObject](/reference/spatial-sdk/latest/root/com.meta.spatial.runtime/panel-scene-object). Interaction SDK doesn't know what is displayed on panels, or about Android [Views](https://developer.android.com/reference/android/view/View). It treats each panel as an opaque surface that can receive Select and Scroll pointer events. Panels that have an `IsdkGrabHandle` component will also receive Grab events.

Interaction SDK's `IsdkToolkitBridgeSystem` automatically modifies all Spatial SDK panels in your scene to include Interaction SDK components, so you don't need to make any manual changes to use Interaction SDK's panel features.

## Manually convert a panel into an Interaction SDK panel

 If you disabled the `IsdkToolkitBridgeSystem`, wish to customize panel behavior, or want to add touch limiting to your own custom panel component, you can manually convert a panel into an Interaction SDK panel.

1. Spawn a panel within your scene by completing [Spawn and Remove 2D Panels](/documentation/spatial-sdk/spatial-sdk-2dpanel-spawn).

2. Using either [Spatial Editor](/documentation/spatial-sdk/spatial-editor-components#add-components-to-an-object) or Android Studio, add the following components to the panel entity. Adding these required components to an entity registers it in the `IsdkSystem` as a panel.
    * com.meta.spatial.toolkit.Transform
    * com.meta.spatial.isdk.IsdkPanelDimensions

3. (Optional) Add one or more of the following components to the panel entity to further customize its behavior.
    * com.meta.spatial.toolkit.Visible
    * com.meta.spatial.toolkit.Scale
    * com.meta.spatial.isdk.IsdkCurvedPanel
        * When present, specifies that the panel is shaped as if it was wrapped around the edge of a cylinder, instead of flat.
    * com.meta.spatial.isdk.IsdkGrabbable *and* com.meta.spatial.isdk.IsdkPanelGrabHandle
        * Both objects are required.
        * IsdkGrabbable configures grab behavior (one or two handed grab, etc)
        * IsdkPanelGrabHandle defines the collider shape of the grabbable volume.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-isdk-supporting-systems.md
---
title: Supporting systems in Interaction SDK
description: Learn about the supporting system used by the Interaction SDK feature in Spatial SDK.
last_updated: 2025-04-21
---

The following systems are included in the `IsdkFeature` and are enabled by default.

## IsdkSystem

Drives the main Interaction SDK system and forwards input events to the scene. Enables/Disables the LocomotionSystem based on hovered object state.

Inspects the scene and creates ISDK panel components as required, to match SpatialSDK panels.

Has the following public methods:

* `enableDebugTools(bool)`: When set to true, renders wireframe debug meshes in the scene to help debug interaction issues.
* `registerObserver(observer: (PointerEvent) -> Unit)`: Adds a callback that will be invoked for each pointer event. Can be used in place of InputListener, if you need access to all pointer event fields.

## IsdkDefaultCursorSystem

Renders a reticle on hovered objects. Users can disable this by setting its active flag to false.

```kotlin
systemManager.findSystem<IsdkDefaultCursorSystem>().active = false
```

## IsdkToolkitBridgeSystem

Inspects the scene and creates Interaction SDK grabbable components based on the existing scene hierarchy.

This system can be disabled this by setting its active flag to false.

```kotlin
systemManager.findSystem<IsdkToolkitBridgeSystem>().active = false
```

## IsdkPanelPaddingRenderSystem

Renders a white outline when a panel's grab region is hovered. This system doesn't have any configurable properties.

## IsdkInputListenerSystem

Provides a mechanism for routing input events for all panels and grabbables in the scene to a single `InputListener` instance.

An `InputListener` can be registered with the system via the `setInputListener` method:

```kotlin
systemManager.findSystem<IsdkInputListenerSystem>().setInputListener(...)
```

A usage example can be found in the **object_3d_sample_isdk** sample.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-mruk.md
---
title: Mixed Reality Utility Kit
description: Learn how to use Mixed Reality Utility Kit with Meta Spatial SDK.
last_updated: 2025-04-16
---

***

**Health and Safety Recommendation**: While building mixed reality experiences, we highly recommend evaluating your content to offer your users a comfortable and safe experience. Please refer to the [Health and Safety](/resources/mr-health-safety-guideline/) and [Design](/resources/mr-design-guideline/) guidelines before designing and developing your app using Scene.

***

## Overview

Mixed Reality Utility Kit provides a set of utilities and tools on top of Scene API (not to be confused with [Spatial SDK Scene](/documentation/spatial-sdk/spatial-sdk-scene/)) to perform common operations when building spatial apps. This makes it easier to program against the physical world, and allows you to focus on what makes your app unique.

## How does scene work?

{%include presence-platform-shared/scene-explanation.md %}

## Getting started

### Prerequisites

Include the `meta-spatial-sdk-mruk.aar` and `org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.3` dependencies in your project as [described in the setup tutorial](/documentation/spatial-sdk/spatial-sdk-tutorial-start/). If you are using one of the sample projects, this step is already completed for you.

### Adding the MRUK feature

MR Utility Kit is provided as a [SpatialFeature](/documentation/spatial-sdk/spatial-sdk-spatialfeature/). In order to enable it in your app, add `MRUKFeature` to the list returned by the `registerFeatures` function.

Here is an example:

```kotlin
import com.meta.spatial.core.SpatialFeature
import com.meta.spatial.mruk.MRUKFeature
import com.meta.spatial.vr.VRFeature

class MyActivity : AppSystemActivity() {
  private lateinit var mrukFeature: MRUKFeature

  override fun registerFeatures(): List<AetherFeature> {
    mrukFeature = MRUKFeature(this, systemManager)
    return listOf(VRFeature(this), mrukFeature)
  }
  ...
}
```

### Requesting scene permissions

MR Utility Kit requires the `USE_ANCHOR_API` and `USE_SCENE` permissions to be enabled to access scene data from the device. Open `projects/android/AndroidManifest.xml` and add these permissions:

```
<uses-permission android:name="com.oculus.permission.USE_ANCHOR_API" />
<uses-permission android:name="com.oculus.permission.USE_SCENE" />
```

`USE_SCENE` is a runtime permission. In addition to declaring it in the `AndroidManifest.xml` you must also add code to your app to prompt the user for permission.

Here is an example:

```kotlin
companion object {
  const val TAG = "SampleActivity"
  const val PERMISSION_USE_SCENE: String = "com.oculus.permission.USE_SCENE"
  const val REQUEST_CODE_PERMISSION_USE_SCENE: Int = 1
}

override fun onCreate(savedInstanceState: Bundle?) {
  super.onCreate(savedInstanceState)
  if (checkSelfPermission(PERMISSION_USE_SCENE) != PackageManager.PERMISSION_GRANTED) {
    Log.i(TAG, "Scene permission has not been granted, requesting " + PERMISSION_USE_SCENE)
    requestPermissions(arrayOf(PERMISSION_USE_SCENE), REQUEST_CODE_PERMISSION_USE_SCENE)
  } else {
    // Scene permissions already granted, safe to access scene data
  }
}

override fun onRequestPermissionsResult(
    requestCode: Int,
    permissions: Array<out String>,
    grantResults: IntArray
) {
  if (requestCode == REQUEST_CODE_PERMISSION_USE_SCENE &&
      permissions.size == 1 &&
      permissions[0] == PERMISSION_USE_SCENE) {
    val granted = grantResults[0] == PackageManager.PERMISSION_GRANTED
    if (granted) {
      Log.i(TAG, "Use scene permission has been granted")
      // Safe to access scene data
    } else {
      Log.i(TAG, "Use scene permission was DENIED!")
      // Scene data not accessible
    }
  }
}
```

Wait until permission is granted before attempting to load scene data. As this is an asynchronous operation, you must wait until the `onRequestPermissionsResult` callback is received. Handle cases where the user denies permission by implementing a suitable fallback.

## Loading scene data

Once you have permission to access scene data, you can call `loadSceneFromDevice` from the `MRUKFeature` class:

```kotlin
var future = mrukFeature.loadSceneFromDevice()

future.whenComplete { result: MRUKLoadDeviceResult, _ ->
  Log.i(TAG, "Load scene from device result: ${result}")
}
```

`loadSceneFromDevice` returns a `CompletableFuture`. This is an asynchonous operation. You must wait until the operation is completed before attempting to access the data. Use the `whenComplete` method to do this.

### JSON data

You can load scene data from a JSON string, in addition to loading it from your device. This can be useful for testing how your app will behave in a variety of different rooms without being physically present.

Here is an example:

```kotlin
val file = applicationContext.assets.open("scene.json")
val text = file.bufferedReader().use { it.readText() }
mrukFeature.loadSceneFromJsonString(text)
```

Unlike `loadSceneFromDevice`, this is a synchronous operation. You can access the data immediately after calling it.

## Accessing the scene data

Once you have loaded the scene data (either from device or from JSON), you can access it through the `rooms` property on the `MRUKFeature` class. This provides a list of `MRUKRoom` instances. Each room has an `anchors` property, which is a list of entities. Each entity has a `Transform` and `MRUKAnchor` component associated with it. It optionally has a `MRUKPlane` and/or `MRUKVolume` component.

Here is an example of how to iterate over the data and print it out:

```kotlin
for (room in mrukFeature.rooms) {
  Log.d("MRUK", "Room ${room.anchor}")
  for (anchorEntity in room.anchors) {
    val anchor = anchorEntity.getComponent<MRUKAnchor>()
    Log.d("MRUK", "Anchor: ${anchor.uuid}, labels: ${anchor.labels}")
    val transform = anchorEntity.getComponent<Transform>()
    Log.d("MRUK", "Transform: ${transform.transform}")
    val plane = anchorEntity.tryGetComponent<MRUKPlane>()
    if (plane != null) {
      Log.d("MRUK", "Plane min: ${plane.min}, max: ${plane.max}, boundary: ${plane.boundary}")
    }
    val volume = anchorEntity.tryGetComponent<MRUKVolume>()
    if (volume != null) {
      Log.d("MRUK", "Volume min: ${volume.min}, max: ${volume.max}")
    }
  }
}
```

You can use `Query` to find entities without going through the `MRUKFeature` class. This is described in the [ECS documentation](/documentation/spatial-sdk/spatial-sdk-ecs/).

## AnchorMeshSpawner

`AnchorMeshSpawner` provides a convenient way to spawn [glTF](/documentation/spatial-sdk/spatial-sdk-gltfs/) meshes that are scaled and positioned to match the bounds of a `MRUKVolume` or `MRUKPlane`. This allows you to create virtual representations of your furniture and have them appear in the same location as your physical furniture.

Here is an example:

```kotlin
val meshSpawner: AnchorMeshSpawner =
    AnchorMeshSpawner(
        mrukFeature,
        mapOf(
            MRUKLabel.TABLE to AnchorMeshSpawner.AnchorMeshGroup(listOf("Furniture/Table.glb")),
            MRUKLabel.COUCH to AnchorMeshSpawner.AnchorMeshGroup(listOf("Furniture/Couch.glb")),
            MRUKLabel.WINDOW_FRAME to AnchorMeshSpawner.AnchorMeshGroup(listOf("Furniture/Window.glb")),
            MRUKLabel.DOOR_FRAME to AnchorMeshSpawner.AnchorMeshGroup(listOf("Furniture/Door.glb")),
            MRUKLabel.OTHER to AnchorMeshSpawner.AnchorMeshGroup(listOf("Furniture/BoxCardBoard.glb")),
            MRUKLabel.STORAGE to AnchorMeshSpawner.AnchorMeshGroup(listOf("Furniture/Storage.glb")),
            MRUKLabel.BED to AnchorMeshSpawner.AnchorMeshGroup(listOf("Furniture/TwinBed.glb")),
            MRUKLabel.SCREEN to
                    AnchorMeshSpawner.AnchorMeshGroup(listOf("Furniture/ComputerScreen.glb")),
            MRUKLabel.LAMP to AnchorMeshSpawner.AnchorMeshGroup(listOf("Furniture/Lamp.glb")),
            MRUKLabel.PLANT to
                    AnchorMeshSpawner.AnchorMeshGroup(
                        listOf(
                            "Furniture/Plant1.glb",
                            "Furniture/Plant2.glb",
                            "Furniture/Plant3.glb",
                            "Furniture/Plant4.glb")),
            MRUKLabel.WALL_ART to AnchorMeshSpawner.AnchorMeshGroup(listOf("Furniture/WallArt.glb")),
        ))
meshSpawner.spawnMeshes(room)
```

## AnchorProceduralMesh

`AnchorProceduralMesh` provides a way to create a procedural mesh that matches the 2D plane boundary of an anchor. This is useful for creating meshes for the floor, ceiling, and walls. You can supply a custom material.

Here is an example:

```kotlin
val floorMaterial =
    Material().apply { baseTextureAndroidResourceId = R.drawable.carpet_texture }
val wallMaterial = Material().apply { baseTextureAndroidResourceId = R.drawable.wall_texture }
val procMeshSpawner: AnchorProceduralMesh =
    AnchorProceduralMesh(
        mrukFeature,
        mapOf(
            MRUKLabel.FLOOR to AnchorProceduralMeshConfig(floorMaterial, false),
            MRUKLabel.CEILING to AnchorProceduralMeshConfig(wallMaterial, false),
            MRUKLabel.WALL_FACE to AnchorProceduralMeshConfig(wallMaterial, false),
        ))
procMeshSpawner.spawnMeshes(room)
```

## Raycasting

The `MRUKFeature` allows raycasting against a room. You can query for hits starting from a specified origin and direction, typically a head or controller pose. The`raycastRoom` function returns the first hit encountered within the room or null if no hit is found. The `raycastRoomAll` returns all hits as a collection. The result is of type `MRUKHit` and provides the distance, position, and normal of a hit.

Here's an example of querying for hits from the right hand to the current room:
```kotlin
val hits =
    mrukFeature.raycastRoomAll(
        currentRoom.anchor.uuid,
        rightHandPose.t,
        rightHandDirection,
        maxDistance,
        surfaceMask)

```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-ovrmetrics.md
---
title: OVR Metrics Tool for Spatial SDK
description: Meta Spatial SDK supports OVR Metrics Tools Feature.
last_updated: 2024-09-25
---

Spatial SDK integrates seamlessly with the [OVR Metrics Tool](/documentation/native/android/ts-ovrmetricstool/), allowing users to monitor and customize metrics for their apps. The OVR Metrics Tool is a performance monitoring tool for Meta Quest headsets. It provides various metrics such as framerate, heat, and GPU and CPU throttling values. You can add custom metrics or messages to the OVR Metrics Tool, display them in real-time, and record them to CSV files for later analysis.

## Setting up

Before getting started with the OVR Metrics Tool, follow these steps to get setup:

1. Install the latest version from the [Meta Horizon Store](https://www.meta.com/experiences/ovr-metrics-tool/2372625889463779/). Or search for ovr metrics tool and download the app from the App Store on headset.
2. [Enable the desired monitoring configurations](/documentation/native/android/ts-ovrmetricstool/#collect-performance-data-with-ovr-metrics-tool) in the OVR Metrics Tool settings, such as overlay messages or CSV recording.

![OVR Metrics Tool](/images/fa_aether_ovrmetrics.png)

## Usage

You can use the OVR Metrics Tool to capture predefined metrics, create new customized metrics, record debug data to a CSV file, and append custom developer data into the CSV.

### Spatial SDK predefined metrics

You can register the ```OVRMetricsFeature``` in your app to add predefined metrics of interest, as in the following example:

```kotlin
// override this in your activity
override fun registerFeatures(): List<SpatialFeature> {
  return listOf(..., OVRMetricsFeature(this,
            this,
            OVRMetricsDataModel() {
              numberOfMeshes()
              numberOfPanels()
              numberOfGrabbables()
            },
            OVRMetricsScene({ scene }) {
              viewOrigin()
              viewRotationX()
              numberOfObjects()
              numberOfAnchors()
            },
            OVRMetricsNetwork({ networkStatsDisplaySystem.networking }) {
              rtt()
              packetLoss()
            }))
}
```

You can check our sample app [**Custom Components Sample**](https://github.com/meta-quest/Meta-Spatial-SDK-Samples/tree/main/CustomComponentsSample), which showcases real-time metrics utilizing OVR Metrics Tool.

![OVR Metrics Tool](/images/fa_aether_ovrmetrics_network.png)

#### Existing metrics

Spatial SDK categorizes metrics into groups such as 3DScene, DataModel, and Network. Each group includes specific metrics like:

* **Spatial Scene Metrics**: viewOrigin, viewRotationX, numberOfObjects, etc.
* **Spatial DataModel Metrics**: numberOfMeshes, numberOfPanels, numberOfGrabbables.
* **Spatial Network Metrics**: rtt, packetLoss, sendBandwidth, receiveBandwidth.

### Create new customized metrics

You can also define app-specific metrics. For example, the **OVRMetricsScene** metrics group can create its own metrics as shown below:

```kotlin
class OVRMetricsScene(val getScene: () -> Scene?, init: OVRMetricsScene.() -> Unit = {}) : OVRMetricsGroup() {

  val groupName = "SpatialScene"

  init {
    init()
  }

  fun numberOfObjects(): OVRMetricsScene {
    metrics.add(
        OVRMetric(
            OVRMetricDefinition(
                Name = "number_of_objects",
                DisplayName = "Obj#",
                Group = groupName,
                RangeMin = 0,
                RangeMax = 1000),
            { getScene()?.getNumberOfObjects() ?: 0 }))
    return this
  }

  fun viewOrigin(): OVRMetricsScene {
    overlayMessages.add({
      val pos = getScene()?.getViewOrigin() ?: Vector3(0f)
      val formater = DecimalFormat("#,##0.00")
      "Pos: (${formater.format(pos.x)}, ${formater.format(pos.y)}, ${formater.format(pos.z)})"
    })
    return this
  }

  ...
}
```

In OVR Metrics Tool, there are two distinct categories of customized metrics. The first category presents metrics in the form of diagrams and numerical values, while the second category displays string messages in an overlay format.

1. **Diagrams and numbers**: This includes the metrics definition (display name, the range, etc) and the function that generates the values in runtime (for example, **numberOfObjects**).
2. **String message in overlay**: This uses a function to generate a string that's appended to the overlay message automatically (for example, **viewOrigin**).

### Publish debug strings

The OVR Metrics Tool also supports APIs for publishing debug strings on overlays or CSV files:

```kotlin
import com.meta.spatial.ovrmetrics.OVRMetricsTool

// Set the overlay debug string
OVRMetricsTool.setOverlayDebugString("Debug String")

// Append debug string to CSV files
OVRMetricsTool.appendCsvDebugString("Debug String")

```

![OVR Metrics Tool](/images/fa_aether_ovrmetrics_overlay.png)

For more information on publishing debug strings, see [append CSV debug string](/documentation/native/android/ts-ovrmetricstool/#append-csv-debug-string).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-packages.md
---
title: Meta Spatial SDK Packages
description: Page listing the available Meta Spatial SDK Packages.
last_updated: 2024-09-22
---

All Spatial SDK packages are licensed under the [Meta Platform Technologies SDK License Agreement](https://developer.oculus.com/licenses/oculussdk/).

Here is a full list of all the available packages with a short summary explaining each one.

### meta-spatial-sdk

```
com.meta.spatial:meta-spatial-sdk:VERSION
```

The core Spatial SDK package, required for all projects.

### meta-spatial-sdk-vr

```
com.meta.spatial:meta-spatial-sdk-vr:VERSION
```

Virtual reality related functionality, necessary for most apps.

### meta-spatial-sdk-toolkit

```
com.meta.spatial:meta-spatial-sdk-toolkit:VERSION
```

The toolkit package, contains many useful Components and Systems frequently used in apps.

### meta-spatial-sdk-physics

```
com.meta.spatial:meta-spatial-sdk-physics:VERSION
```

Physics support for Spatial SDK, more info on the [physics page](/documentation/spatial-sdk/spatial-sdk-physics/).

### meta-spatial-sdk-ovrmetrics

```
com.meta.spatial:meta-spatial-sdk-ovrmetrics:VERSION
```

Easily view performance stats and information about your scene, more info on the [OVRMetrics page](/documentation/spatial-sdk/spatial-sdk-ovrmetrics/).

### meta-spatial-sdk-castinputforward

```
com.meta.spatial:meta-spatial-sdk-castinputforward:VERSION
```

Develop your app without needing to constantly don/doff your headset, more info on the [Input Forwarding page](/documentation/spatial-sdk/spatial-sdk-tooling-castinputforward/).

### meta-spatial-sdk-mruk

```
com.meta.spatial:meta-spatial-sdk-mruk:VERSION
```

Make compelling Mixed Reality experiences with the Mixed Reality Utility Kit, more info on the [MRUK page](/documentation/spatial-sdk/spatial-sdk-mruk/).

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-passthrough.md
---
title: Passthrough
description: Meta Spatial SDK Passthrough
last_updated: 2024-11-18
---

Passthrough provides a real-time, perceptually comfortable 3D visualization of the physical world in a Meta Quest headset. The Passthrough API allows developers to integrate passthrough with their virtual experiences.

## Activating passthrough

Use the following code snippet to enable passthrough:

```kotlin
// setting this to false would disable passthrough
scene.enablePassthrough(true)
```

To view the passthrough feed, pair this action with toggling the visibility of your skybox.

## Passthrough LUTs

Passthrough lookup tables (LUTs) transform the colors that passthrough displays. You can use them to evoke a certain style, such as tinting everything red when you are low on health, or to emulate a lighting environment, like dimming lights when a movie starts.

![LUT Mapping of a 16^3 RGB cube](/images/fa_aether_mr_2.png)

> The image above is from an article called [LUTs vs Transforms: How They’re Different and Why It Matters](https://blog.frame.io/2020/04/27/luts-vs-transforms/), which provides a good explanation of LUTs.

This image compares the appearance of an image before and after applying a passthrough LUT:

![Showing a before and after of applying a LUT](/images/fa_aether_mr.png)

> [Image credit](https://www.inpixio.com/blog/hdr/best-free-and-paid-luts/)

The API for Meta Quest maps input RGB values with components ranging from zero to 15, to output RGB values, ranging from zero to 255. This process is equivalent to mapping a low resolution 16x16x16 RGB cube to a high resolution 256x256x256 cube. For instance, you can map the input hex of F3A to F030A0 to obtain a roughly equivalent value.

The following example demonstrates setting up and using a LUT. This app dims the scene by transforming the RGB values to approximately 1/4 of their original settings. The app achieves this by multiplying the components by four, which is a 1/4th of 16. This value is the multiplier required to obtain a roughly equivalent color.

```kotlin
// initialize lut
val tbl = Lut()
for (r in 0..15) {
    for (g in 0..15) {
        for (b in 0..15) {
            // set a mapping color for each RGB value in the (0-15)^3 range
            tbl.setMapping(r, g, b, r * 4 + r / 4, g * 4 + g / 4, b * 4 + b / 4)
        }
    }
}

// apply it to the passthrough
scene.setPassthroughLUT(tbl)
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-pca-kotlin-api.md
---
title: Android Camera2 API
description: Camera Access to Quest 3 and Quest 3s is via the Android Camera2 API, which is included in the NDK.
last_updated: 2025-04-29
---

{% include passthrough-shared/pca-overview-shared.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-pca-overview.md
---
title: Passthrough Camera Access Overview
description: Camera Access to Quest 3 and Quest 3s is via the Android Camera2 API, which is included in the NDK.
last_updated: 2025-04-29
---

{% include passthrough-shared/pca-kotlin-documentation.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-physics.md
---
title: Physics
description: Meta Spatial SDK's tutorial on the physics feature
last_updated: 2024-11-25
---

## Overview

By default, Spatial SDK objects don't simulate real-world physics and lack physical properties like collision detection and gravity. For instance, objects cannot collide with other objects, free fall when placed above the ground, and other common physical behaviors. To mimic real-world physics, Spatial SDK provides you with a way to set up and configure the physics engine and enable physics for entities.

## PhysicsFeature

Registering `PhysicsFeature` is the starting point for setting up physics. Add `PhysicsFeature` to the list of features defined in the `registerFeatures` hook of your main activity:

```kotlin
import com.meta.spatial.physics.PhysicsFeature

override fun registerFeatures(): List<SpatialFeature> {
  return listOf(PhysicsFeature(spatial))
}
```

Behind the scenes, the Meta Spatial app runtime will initiate the work of setting up the physics engine, creating the physics objects, and more.

## Physics component

Attach the `Physics` component to an entity to enable physics.

Consider the following example:

```kotlin
val box =
    Entity.create(
        listOf(
            Mesh(Uri.parse("mesh://box")),
            Box(Vector3(-0.5f), Vector3(0.5f)),
            Grabbable(),
            Physics(
                density = 0.5f,
                restitution = 0.25f,
                friction = FrictionObject(1f, 0f, 0f)),
            Transform(Pose(Vector3(-2.0f, 20.0f, 0.0f), Quaternion.getRandomQuat()))
            )
        )
```

This example creates an entity with a `Physics` component that specifies the density, restitution, and friction of the physics object.

### Physical properties

Here is a breakdown of the `Physics` class constructor:

```kotlin
class Physics(
    shape: String = "box",
    linearVelocity: Vector3 = Vector3(0.0f),
    angularVelocity: Vector3 = Vector3(0.0f),
    dimensions: Vector3 = Vector3(0.5f),
    density: Float = 1.0f,
    restitution: Float = 0.2f,
    friction: FrictionObject = FrictionObject(0.5f, 0f, 0f),
    state: PhysicsState = PhysicsState.DYNAMIC,
    applyForce: Vector3 = Vector3(0.0f),
) : ComponentBase() {
    ...
}
```

Spatial SDK currently supports only rigid body physics, and all units are in the metric system (meters, kilograms, Newtons).

- `shape`: the geometric shape of the physics object you want to simulate. Supported shapes include `box`, `sphere`, and custom shapes. For simple custom shapes, you should pass the [URI](https://developer.android.com/reference/android/net/Uri) of the glTF file to the `shape` parameter.
- `linearVelocity`: the linear velocity of the physics object.
- `angularVelocity`: the angular velocity of the physics object.
- `dimensions`: the dimensions of the physics object. This parameter specifies the length (`dimensions.x`), height (`dimensions.y`), and width (`dimensions.z`) for a box shaped object as well as the radius (`dimensions.x`) for a sphere object.
- `density`: the mass density of the physics object. The mass of a physics object is the product of its density and its volume.
- `restitution`: a measure of the collision elasticity with the physics object.
- `friction`: the friction of the physics object. The friction object contains three floating numbers to represent different friction coefficients: `slidingFriction`, `rollingFriction`, and `spinningFriction`.
- `state`: the simulation state of the physics object, with possible values being: `dynamic`, `static` and `kinematic`. `dynamic` means the physics object can be affected by forces and collisions. `static` means the physics object cannot be affected by forces but can collide. `kinematic` means the physics object cannot affected by forces but can move and cause collisions.
- `applyForce`: the external force to apply to the physics object.


Custom shapes should be used sparingly. Simulating physics for a complicated glTF model degrades performance significantly. Use low-poly models instead of complex ones.

## Physics simulation

After registering the `PhysicsFeature` and attaching the `Physics` components to the entities, the app automatically starts the physics simulation when the app runs.

## Miscellaneous

`PhysicsFeature` is configurable. You can also add a `PhysicsOutOfBoundsSystem` to your application if you want to set boundaries for the physics objects.

### PhysicsFeature configurations

When registering `PhysicsFeature`, you can specify whether to enable grabbable physics.

You can configure it like this:

```kotlin
class PhysicsFeature(val spatial: SpatialInterface, val useGrabbablePhysics: Boolean = true) :
    SpatialFeature {
    ...
}
```

When grabbable physics is enabled, grabbed physics entities will have a physics state of `kinematic`, meaning they cannot be affected by external forces. If grabbable physics is disabled, grabbed physics entities will retain their physics state, be it `static`, `dynamic` or `kinematic`.

### PhysicsOutOfBoundsSystem

By default, a Meta Spatial app does not set any boundaries in the physics environment. If you want to clean up or destroy entities that are out of the bounds, you can use the `PhysicsOutOfBoundsSystem`.

Here's an example implementation of `PhysicsOutOfBoundsSystem`. This system automatically removes entities that are 100 meters below the origin point of the scene:

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    // Add a system to remove objects that fall out of bounds
    systemManager.registerSystem(
        PhysicsOutOfBoundsSystem(spatial).apply { setBounds(minY = -100.0f) })
}
```

You can define the bounds of the physics world using the `setBounds` method in the `PhysicsOutOfBoundsSystem`:

```kotlin
public fun setBounds(
    minX: Float? = null,
    maxX: Float? = null,
    minY: Float? = null,
    maxY: Float? = null,
    minZ: Float? = null,
    maxZ: Float? = null
) {
    this.minX = minX
    this.maxX = maxX
    this.minY = minY
    this.maxY = maxY
    this.minZ = minZ
    this.maxZ = maxZ
}
```

Meta Spatial apps use a left-handed 3D coordinate system. The positive x-axis points to the right. The positive y-axis points up. The positive z-axis points away from the screen.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-queries.md
---
title: Queries
description: A Meta Spatial SDK tutorial on Queries
last_updated: 2025-04-22
---

## Overview

In Spatial SDK applications, you may want to write different systems to apply logic to specific entities. For example, consider a scenario where you need to update physics, trigger collision callbacks, or apply game logic to all entities that have a `Physics` component. Instead of manually iterating over all the entities in a Spatial SDK application, Queries provides a unified interface to access the relevant entities.

Queries are an essential tool when writing systems for a Spatial SDK application. They enable dynamic retrieval of entities based on specific component criteria. You don't have to worry about the details of how entities are retrieved.

## Query creation

Here is a simple example of creating a `Query`:

```kotlin
val q: Query = Query.where { has(Physics.id) }
```

The query system is initiated by creating a query object that filters entities based on specific criteria. For this query, the entities must have a `Physics` component.

## Query evaluation

Once the query is defined, it can be evaluated by invoking the `eval` method:

```kotlin
val entities: Sequence<Entity> = q.eval()
```

Under the hood, the query won't run until `eval` is invoked.


## Query operators

There are two categories of operators in a query: conditional and logical operators.

### Conditional operators

These operators check for specific conditions or states.
- The `has` operator checks if the entity has certain types of component.
- The `changed` operator checks if certain components of the entity have changed in the last tick.

### Logical operators

These operators are used to combine conditions or logical expressions.
- The `and` operator is used to "and" the two conditions on either side.
- The `or` operator is used to "or" the two conditions on either side.

You can create complex queries by mixing and matching the four query operators.

```kotlin
val q: Query = Query.where { has(Scale.id) and changed(Scale.id, Mesh.id, Panel.id) }
```

Once evaluated, this query will return a list of entities that have the `Scale` component, and whose attributes of the `Scale`, `Mesh`, and `Panel` components have changed since the last tick.

## Filtering in queries
You can refine your query results by applying filters.

```kotlin
val droneEntities =
    Query.where { has(DroneComponent.id, Transform.id) }
        .filter { by(DroneComponent.enabledData).isEqualTo(true) }
        .eval()
```
In this example:
1. The query first selects entities that have both DroneComponent and Transform components.
2. The filter method is then used to ensure that only entities with boolean attribute `enabled` set to true are included in the results.
3. The eval method executes the query, returning a sequence of entities that meet all specified criteria.

For more information about query filtering, refer to [Filters](/documentation/spatial-sdk/spatial-sdk-filters/).

### Sorting query results

You can sort the results of a query by using the `sort` method.

```kotlin
// Sort by rotation speed, descending, and take the first 10 results, if any
val sortedEntities =
    Query.where { has(DroneComponent.id, Transform.id) }
        .filter { by(DroneComponent.enabledData).isEqualTo(true) }
        .sort {
            with {
                by(DroneComponent.rotationSpeedData).desc()
            }
            take(0, 10)
        }
        .eval()
```

In this example:
1. The query first selects entities that have both `DroneComponent` and `Transform` components.
2. The `filter` method is then used to ensure that only entities with boolean attribute `enabled` set to true are included in the results.
3. The `sort` method is then used to sort the results by the `rotationSpeed` float attribute in descending order.
4. The `take` method is used to limit the results to the first 10 entities.
5. The `eval` method executes the query, returning a sequence of entities that meet all specified criteria.

For more information about query sorting, refer to [Sorting](/documentation/spatial-sdk/spatial-sdk-sorting/).

## Recommendation

Queries should generally be used in either [systems](/documentation/spatial-sdk/spatial-sdk-writing-new-system/) or App lifecycle hooks.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-runtime-guidelines.md
---
title: Runtime guidelines
description: Meta Spatial SDK Runtime guidelines categorized by CPU, GPU, and memory.
last_updated: 2024-10-16
---

## Overview

This page categorizes guidelines into related groups. For instance, CPU capacity limits the number of panels you can have at the default texture size. This limitation means the type of content you have in panels directly influences how many panels Meta Quest devices can support.

### CPU

There are a few CPU-limited tasks that trade-off with each other. In general, your app can pick any linear combination of objects and panels as described below:

#### Objects

| **Object type**                  | **Max number at 90 FPS** | **Details**                                                                           |
|----------------------------------|--------------------------|---------------------------------------------------------------------------------------|
| EOPT (Entity Operation Per Tick) | 2,000                    | A read or write to the data model inside of a system                                  |
| Physics object                   | 500                      | A simple GLB that includes Physics. Typically, graphics are more of a bottleneck here |

#### Panels

| **Panel type**       | **Estimated number of open panels (of panel type) before FPS dips temporarily below 90 on each additional panel spawn, in isolation** | **Estimated number of open panels (of panel type) before FPS stays below 90 while running in isolation** |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Empty view panel     | 20                                                                                                                                    | 40                                                                                 |
| UI (only) view panel | 15                                                                                                                                    | 40                                                                                 |
| Image view panel     | 15                                                                                                                                    | 40                                                                                 |
| Web view panel       | 5                                                                                                                                     | 30                                                                                 |
| Video view panel     | 3                                                                                                                                     | 5                                                                                  |
| Activity-based panel | 2                                                                                                                                     | 2                                                                                  |
| Panel with layers    | 5                                                                                                                                     | 15                                                                                 |

### GPU

The primary GPU limitations are:

- The number of 3D GLB objects that can be in view simultaneously.
- The amount of space objects cumulatively take up in the user’s viewport.

Considering these limitations, a maximum of 100 objects when they occupy more than 50% of the viewport is recommended. Use fewer objects to take up more of the viewport. If you need to use more objects, ensure you take up less than 50% of the viewport.

Panels can also bottleneck GPU utilization as their resolution size increases. Spatial SDK defines resolutions in terms of the percentage of the screen relative to your device’s PPD (pixel per degree). The relationship between GPU utilization and pixel resolution tends to scale linearly when bound to the fill rate. For example, using a default-sized panel of approximately half the screen size will give you a resolution of 1000 by 750 pixels. Each additional 480,000 pixels will use an extra 1% of your GPU.

This configuration doesn’t scale perfectly linearly, but we’ve been able to create examples in production where we’ve rendered panels at 25 million pixels using this calculation.

### Memory

Approximately 1,000 objects in the scenegraph are supported, as long as they don’t exceed the GPU and CPU limitations.

### Example usage calculation

Using the information above, you should be able to mix and match limits to estimate how complex your app can be in each compute category. Here’s an example of an app that would fit inside our performance envelope:

- You have eight hundred objects in the scene representing the scenery, birds, environment, flowerbeds, and flowers.
- Through object management, you simultaneously show no more than sixty objects in the viewport.
- You reserve two hundred EOPTs at any tick for growing flowers.
- You have one activity-based panel representing a game ported from Android.
- You have three UI panels for UI instructions, alerts, and settings.

#### CPU usage calculation

| **Feature count**      | **Max allotment of each feature** | **Percentage of compute usage** |
|------------------------|-----------------------------------|---------------------------------|
| 200 EOPTs              | 2,000 EOPT                        | 10%                             |
| 1 Activity-based panel | 2 Activity-based panels           | 50%                             |
| 3 UI view panels       | 15 UI view panels                 | 20%                             |
| Total estimated usage  |                                   | 80% CPU usage                   |

#### GPU usage calculation

| **Feature count**                                             | **Max allotment of each feature** | **Percentage of GPU usage** |
|---------------------------------------------------------------|-----------------------------------|-----------------------------|
| 60 objects in the viewport                                    | 100 objects in the viewport       | 60%                         |
| 4 standard (1000 x 750) panels that take up 50% of the screen | 48,000,000 pixels*                | 6.25%                       |
| Total estimated usage                                         |                                   | 66.25% GPU usage            |

*_This is a rough estimate for max pixels. Please test your apps for the best results._

#### Memory usage calculation

| **Feature count**             | **Max allotment of each feature** | **Percentage of memory usage** |
|-------------------------------|-----------------------------------|--------------------------------|
| 800 objects in the scenegraph | 1,000 objects in the scenegraph   | 80%                            |
| Total estimated usage         |                                   | 80% memory usage               |

Given these calculations, this example app still has plenty of computing power remaining to add new features and extend the experience in the future while maintaining a steady frame rate above 90 FPS.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-scene.md
---
title: Scene
description: The scene is Meta Spatial SDK’s representation of the 3D environment in your app.
last_updated: 2024-11-11
---

## Overview

The term "scene" refers to Spatial SDK's representation of a 3D environment in your app. Spatial SDK applications use the metric system for everything in 3D, where one unit is equal to one meter, kilogram, newton, etc. Features, like [physics](/documentation/spatial-sdk/spatial-sdk-physics), are designed to work only with the metric system. Spatial SDK also uses a left-handed coordinate system, with X+ being right, Y+ being up, and Z+ being forward.

## Understanding the `Scene` class

The `Scene` class provides an API that enables interaction with your local 3D environment. Any actions you perform here will only affect the client running the code and will not propagate to other clients.

The key elements of the API are detailed in the following sections.

### `setViewOrigin`

This attribute sets the client's position and rotation in the virtual world. It can be useful for implementing a locomotion system.

### `setLightingEnvironment(amientColor, sunColor, sunDirection, environmentIntensity)`

This method controls the lighting in your app.

- `ambientColor`: The base color to add to everything (even when there is no light).
- `environmentIntensity`: Controls how intense the current Image Based Lighting (IBL) is. The default is 1.0f.
- `sunColor`: The color tint the virtual sun should have.
- `sunDirection`: The direction in which you want the light to point.

### `enablePassthrough`

This attribute enables passthrough. See the [Passthrough page](/documentation/spatial-sdk/spatial-sdk-passthrough/) for more information.

### `drawDebugLine(from, to, color, displayCount)`

This method displays a small line in the scene from the `from` parameter to the `to` parameter for the number of frames specified by `displayCount`. This method is helpful for debugging values or creating pointers.

### `updateIBLEnvironment(envFilename)`

This method sets the lighting environment to the `.env` file path, which is relative to the assets folder. See the [Environment page's information on image based lighting](/documentation/spatial-sdk/spatial-sdk-environment#image-based-lighting) for more details.

### Sound APIs (`playSpatialSound` and more):

The Audio API supports spatial audio, enhancing a sense of realism in your VR app. For more information, see the [Audio](/documentation/spatial-sdk/spatial-sdk-audio/) page.

### `lineSegmentIntersect(from, to)`

This method traverses the line segment created from the `from` parameter to the `to` parameter and returns the `HitInfo?` value of the first mesh it intersects in the scene. This method helps capture what a user may be pointing at.

### `setDepthParams(minDepth, maxDepth)`

This method specifies the near and far plane distances, in meters, in the view frustum. Decrease `minDepth` if meshes, such as controllers, are clipping because they’re too close to the camera. Increase `maxDepth` if things aren’t appearing because they are too far away.

### `setReferenceSpace`

This method allows you to specify the [OpenXR reference space](https://registry.khronos.org/OpenXR/specs/1.1/html/xrspec.html#spaces-reference-spaces) in your app. This reference space affects how you spawn in your app and how recentering behaves. By default, Spatial SDK uses the `STAGE` reference space. This is a world-relative reference space and is well suited for mixed reality apps using Mixed Reality Utility Kit. However, in this space, recentering doesn't do anything, since the world around you is not physically moving. If you would like to attach custom logic to when the user presses the recenter button, you can override `VRActivity.onRecenter`.

`LOCAL_FLOOR` is the recommended space to use in most virtual reality apps as recentering should work as expected out of the box. To set your app's reference space to `LOCAL_FLOOR`, simply add this line to your app's `onSceneReady()`:

```kotlin
scene.setReferenceSpace(ReferenceSpace.LOCAL_FLOOR)
```

## Interacting with `Scene` objects

Typically, dealing with components such as `Mesh`, `Material`, and `Transform` will suffice. However, there may be occasions when you require more control over your objects. In these instances, you will interact with `Scene` objects:

- `SceneObject`: This is an instance of a 3D mesh in a scene, which points to a `SceneMesh`.
- `SceneMesh`: The mesh data, such as vertices. It points to a `SceneMaterial`.
- `SceneMaterial`: This describes the material properties for a mesh, such as roughness and metallicness, and points to a `SceneTexture`.
- `SceneTexture`: The image data used in a material.

Consider the Mesh Component. The `MeshCreationSystem` creates `SceneMaterial`s, `SceneMesh`es, and `SceneObject`s from the data inside the `Mesh` and `Material` components. Dealing with these scene objects enables you to create robust systems like the `MeshCreationSystem`.

## Working with `SceneObject`s

`SceneObject`s allow you to do things like attach input listeners and set the visibility of objects.

To get a `SceneObject` from an `Entity`, follow these steps:

```kotlin
// getSceneObject returns a CompletableFuture<SceneObject>
systemManager.findSystem<SceneObjectSystem>().getSceneObject(myEntity)?.thenAccept {
    sceneObject -> // do something with sceneObject here
}
```

This code will execute on `myEntity` once the `MeshCreationSystem` has loaded it. Models may load asynchronously.

If you want to attach a listener to an object that hides it if the user presses the “A” button while pointing at the object, you can use the following code:

```kotlin
systemManager.findSystem<SceneObjectSystem>().getSceneObject(myEntity)?.thenAccept {
    sceneObject -> sceneObject.addInputListener(
        object: InputListener {
            override fun onInput(
                receiver: SceneObject,
                hitInfo: HitInfo,
                sourceOfInput: Entity,
                changed: Int,
                clicked: Int,
                downTime: Long
            ): Boolean {
                if ((clicked and ButtonBits.ButtonA) != 0) {
                    receiver.setIsVisible(false)
                }
                return false
            }
        }
    )
}
```

You will need to wait for your entity's `Mesh` component to be picked up by the `MeshCreationSystem`, otherwise you will get `null` if you try to get the `SceneObject` before it is set up. Therefore, this approach works best in a system where you can listen for changes on a `Mesh` component.

For more information about handling button presses, see the [Inputs and contollers](/documentation/spatial-sdk/spatial-sdk-inputs-controllers/) page.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-sorting.md
---
title: Sorting in queries
description: A Meta Spatial SDK tutorial on Query sorting.
last_updated: 2025-04-22
---

## Overview

[Queries](/documentation/spatial-sdk/spatial-sdk-queries) and [filters](/documentation/spatial-sdk/spatial-sdk-filters) are used to find entities which meet certain criteria. The entities returned by a query are not necessarily in a useful order. For example, if you want to find the entity with an `IntAttribute` that has the biggest value, you need to sort the entities returned by a query.

## Write a sorting function

A `Query` object has a `sort` API. You can specify the sorting critera by calling the `with` function. You can also specify the number of returned elements using the `take` API. All of these functions are executed on the C++ side, and are much faster than using a Kotlin filter, if you have a large number of entities.

### with API

Inside of the `with` function, you can specify the sorting criteria by calling the `by` function. The `by` function takes a [AttributeData](/documentation/spatial-sdk/spatial-sdk-filters/#attribute-data) object as a parameter.

```kotlin
// Sorts entities by the value of the attribute intAttr
val sortedEntities = Query.where { has(TestComponent.id) }
    .sort {
        with {
            by(TestComponent.intAttrData)
        }
    }
    .eval()
```

### take API

The `take` API takes two integers as a parameter. The first integer represents offset, specifying the number of elements to skip. The second integer is count, specifying the number of elements to return from starting at offset.

```kotlin
// Sorts entities by the value of the attribute intAttr, and returns the first 10 elements
val sortedEntities = Query.where { has(TestComponent.id) }
    .sort {
        with {
            by(TestComponent.intAttrData)
        }
        take(0, 10)
    }
    .eval()
```

### IntAttribute, FloatAttribute, LongAttribute, TimeAttribute

The code below shows how to use `IntAttribute` to sort entities based on the data of the attribute `intAttr`.

```kotlin
// Sorts entities by the value of the attribute intAttr, in ascending order
val sortedEntities = Query.where { has(TestComponent.id) }
    .sort {
        with {
            by(TestComponent.intAttrData).asc()
        }
    }
    .eval()

// Sorts entities by the value of the attribute intAttr, in descending order
val sortedEntities = Query.where { has(TestComponent.id) }
    .sort {
        with {
            by(TestComponent.intAttrData).desc()
        }
    }
    .eval()
```

By default, the sorting order is ascending. You can use the `asc()` and `desc()` functions to specify the sorting order. `FloatAttribute`, `LongAttribute`, and `TimeAttribute` have identical APIs to those of `IntAttribute`.

### StringAttribute

The code below shows how to use `StringAttribute` to filter entities based on the data of the attribute `stringAttr`.

```kotlin
// Sorts entities by the value of the attribute stringAttr, in ascending order
val sortedEntities = Query.where { has(TestComponent.id) }
    .sort {
        with {
            by(TestComponent.stringAttrData).asc()
        }
    }
    .eval()

// Sorts entities by the value of the attribute stringAttr, in descending order, case-insensitively, and returns the first 10 elements
val sortedEntities = Query.where { has(TestComponent.id) }
    .sort {
        with {
            by(TestComponent.stringAttrData).descCaseInsensitive()
        }
        take(0, 10)
    }
    .eval()
```

### Vector2Attribute, Vector3Attribute, Vector4Attribute

The code below shows how to use `Vector4Attribute` to filter entities based on the data of the attribute `vector4Attr`.

```kotlin
// Sorts entities by the value of the attribute vector4Attr's x property, in ascending order
val sortedEntities = Query.where { has(TestComponent.id) }
    .sort {
        with {
            by(TestComponent.vector4AttrData).byX().asc()
        }
    }
    .eval()

// Sorts entities by the value of the attribute vector4Attr's w property, in descending order
val sortedEntities = Query.where { has(TestComponent.id) }
    .sort {
        with {
            by(TestComponent.vector4AttrData).byW().desc()
        }
    }
    .eval()
```

If `byX()`, `byY()`, `byZ()`, or `byW()` is not called, the sorting will be done based on the X property of the vector. `Vector2Attribute`, `Vector3Attribute`, and `Vector4Attribute` have similar APIs to those of `Vector4Attribute`.

### PoseAttribute

The code below shows how to use `PoseAttribute` to filter entities based on the data of the attribute `poseAttr`.

```kotlin
// Sorts entities by the value of the attribute poseAttr's position's x property, in ascending order
val sortedEntities = Query.where { has(TestComponent.id) }
    .sort {
        with {
            by(TestComponent.poseAttrData).byPositionX().asc()
        }
    }
    .eval()

// Sorts entities by the value of the attribute poseAttr's orientation's w property, in descending order
val sortedEntities = Query.where { has(TestComponent.id) }
    .sort {
        with {
            by(TestComponent.poseAttrData).byOrientationW().desc()
        }
    }
    .eval()
```

## Kotlin Sorting vs Native Sorting

The two queries below will return the same results, but the first uses a Kotlin sorting function and the second uses a native sorting function.

```kotlin
val droneEntities0 =
    Query.where { has(DroneComponent.id, Transform.id) }
        .eval()
        .sortedBy { it.getComponent<DroneComponent>().rotationSpeed }

val droneEntities1 =
    Query.where { has(DroneComponent.id, Transform.id) }
        .sort { with { by(DroneComponent.rotationSpeedData) } }
        .eval()
```

For a query with thousands of entities, using a native sorting function can be 100 times more efficient than using a Kotlin filter. This is because `it.getComponent<DroneComponent>()` is a function that creates a new `DroneComponent` object for each entity, and object creation in large numbers is slow in Kotlin. Meanwhile, `.sort { with { by(DroneComponent.rotationSpeedData) } }` is an API that directly accesses the data of the `DroneComponent` on the C++ side, and is much faster than creating a new `DroneComponent` object.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-spatialfeature.md
---
title: SpatialFeature
description: A SpatialFeature enables you to easily integrate readymade features into any of your Spatial SDK apps with only a few lines of code.
last_updated: 2024-10-16
---

## Overview

A `SpatialFeature` is a collection of components, systems, and lifecycle events that you can add to your code. Spatial SDK will execute these at the appropriate time to implement features into any Spatial SDK app.

A `SpatialFeature` allows you to integrate ready-made features into any of your Spatial SDK apps with only a few lines of code. For example, the `Physics` class, which adds realistic interactions to your scene, is a SpatialFeature that you can add to your apps.

## Use registerFeatures to add features to your app

The `registerFeatures` function defines the features you want to include in your app. It is only called and used at startup. Any modifications to the list after the initial startup will not change the registered features.

Here is an example of registering multiple features in an app:

```
import com.meta.spatial.core.SpatialFeature
import com.meta.spatial.physics.PhysicsFeature
import com.meta.spatial.vr.VRFeature

class MyActivity : AppSystemActivity() {
  override fun registerFeatures(): List<SpatialFeature> {
    return listOf(
        PhysicsFeature(spatial),
        VRFeature(this))
  }
  ...
}
```

Using this code, the example Spatial SDK app will have `Physics` capabilities and default VR capabilities.

### When should I make a SpatialFeature?

You should create a `SpatialFeature` if you plan to use a specific feature in multiple apps or want to use it as a code organization method.

### What can I do in a SpatialFeature?

Using a `SpatialFeature` allows you to execute code at different lifecycle points of an Spatial SDK app.

### How do I register components?

Overrid the `componentsToRegister` function to register components required for your feature. `componentsToRegister` returns a list of `ComponentRegistration` objects.

```
override fun componentsToRegister(): List<ComponentRegistration> {
  return listOf(
      ComponentRegistration.createConfig(MyComponent1.Companion, MyComponent1.id, { MyComponent1() }),
      ComponentRegistration.createConfig(MyComponent2.Companion, MyComponent2.id, { MyComponent2() }, sendRate = SendRate.LOW))
}
```

### ComponentRegistration

`ComponentRegistration` objects enable you to define your component's `SendRate`. If your component is essential and needs to be updated every frame, you can leave it as `SendRate.DEFAULT`. If it does not need to be updated every frame, you may benefit from setting the `sendRate` to `SendRate.LOW`.

### Register Systems

Use different functions to register the systems required for your feature depending on when you want your system to run.

You have three options:

- `earlySystemsToRegister`: All systems in the list returned by this function will run first.
- `systemsToRegister`: All systems in the list returned by this function will run next.
- `lateSystemsToRegister`: All systems in the list returned by this function will run last.

If you do not know which bucket to put your system in, or if it doesn't matter, use `systemsToRegister`.

```
override fun systemsToRegister(): List<SystemBase> {
  return listOf(MySystem())
}

override fun earlySystemsToRegister(): List<SystemBase> {
  return listOf(MyEarlySystem())
}

override fun lateSystemsToRegister(): List<SystemBase> {
  return listOf(MyLateSystem())
}
```

## Android and Spatial SDK lifecycle events

Using a `SpatialFeature`, you can override most traditional Android lifecycle event functions, and some Spatial SDK specific lifecycle events. These functions will execute when the corresponding Android/Spatial SDK lifecycle event occurs.

You can override these functions by using a `SpatialFeature`:

- `onCreate`
- `onSceneReady`
- `onStart`
- `onResume`
- `onPauseActivity`
    - This is only called when extending `VrActivity`, not `VrService`, as services do not utilize `OnPause()`.
- `onStopActivity`
    - This is only called when extending `VrActivity`, not `VrService`, as services do not utilize `OnStop()`.
- `onDestroy`
- `onVRReady`
- `onVRPause`

Here is an example:

```
// Example init code
override fun onSceneReady() {
  Entity.create(listOf(MyComponent()))
  // Other initialization code here
  ...
}
```

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-tooling-castinputforward.md
---
title: Input forwarding
description: Work on your Meta Spatial SDK app without needing to put on your headset.
last_updated: 2024-09-16
---

It can be frustrating to constantly put your headset on and take it off during development. With input forwarding, you can move around your scene, click-and-drag on panels, and even grab objects in your 3D scene. All without needing to put on your headset.

Here's a quick example of what it looks like in action:

<section>
    <embed-video width="100%">
        <video-source handle="GEGSUwJ2OucB9cUBAIOvqA8yMLR8bosWAAAF" />
    </embed-video>
</section>

## Setup

Input forwarding is accessible through the cast functionality in Meta Quest Developer Hub (MQDH). [Download MQDH](https://developer.oculus.com/meta-quest-developer-hub/) to get started. You must be on MQDH version 5.0 or later for this feature to work.

## Adding input forwarding

If you are starting with one of the sample projects, this has already been set up for you.

1. Add the `meta-spatial-sdk-castinputforward` dependency

    In your Spatial SDK app you can add input forwarding support by adding the following dependency in your `app/build.gradle.kts` file:

    ```
    implementation("com.meta.spatial:meta-spatial-sdk-castinputforward:$metaSpatialSdkVersion")
    ```

    If you are using Groovy (`build.gradle`):

    ```
    implementation "com.meta.spatial:meta-spatial-sdk-castinputforward:$metaSpatialSdkVersion"
    ```

2. Verify your app has `buildConfig` enabled

    `build.gradle.kts`:

    ```
    android {
      ...

      buildFeatures {
       buildConfig = true
      }
    }
    ```

    `build.gradle`:

    ```
    android {
      ...

      buildFeatures {
       buildConfig true
      }
    }
    ```

3. Modify your `AndroidManifest.xml`

    In your manifest file, add the following `uses-native-library` tag under the `<application>` section:

    ```xml
    <application>
        ...

        <uses-native-library
            android:name="libossdk.oculus.so"
            android:required="true"
        />
    </application>
    ```

4. Add the `CastInputForwardFeature` to your base immersive activity

    ```diff
      override fun registerFeatures(): List<SpatialFeature> {
        var features = ...
    +   if (BuildConfig.DEBUG) {
    +     features.add(CastInputForwardFeature(this))
    +   }
        return features
      }
    ```

    `CastInputForwardFeature` is only useful during development and so you should not release an app with it included. This is why the `BuildConfig.DEBUG` check is being made.


## Using input forwarding

1. Connect your headset

    Make sure it shows up in MQDH.

    ![Device appears in MQDH](/images/fa_aether_castinputforward_mqdhdevices.png)

2. Start casting with MQDH

    Follow the [Cast headset footage](https://developers.meta.com/horizon/documentation/spatial-sdk/ts-mqdh-media#cast-headset-footage) guide to start casting with MQDH.

3. Run your app

    Make sure that you're building a DEBUG flavor, and run your app in Android Studio.

    ![Build and run in Android Studio](/images/fa_aether_castinputforward_runandroidstudio.gif)

4. Select the input forward icon while inside of your app to enable input forwarding.

    <section>
        <embed-video width="100%">
            <video-source handle="GEGSUwJ2OucB9cUBAIOvqA8yMLR8bosWAAAF" />
        </embed-video>
    </section>

Casting with input forwarding only works with your resolution set to "Original (1:1)", it will not work correctly if your resolution is set to "Cropped (16:9)" or "Cinematic (16:9)".

## Controls

| Key | Action |
| -------- | ------- |
| W / Up Arrow | Move forward |
| S / Down Arrow | Move backward |
| A | Move left |
| D | Move right |
| Q | Move up |
| E | Move down |
| Left Arrow | Rotate left |
| Right Arrow | Rotate right |
| Shift | Sprint |
| Left mouse button | Click |
| Ctrl + Left mouse button / Right mouse button | Hold to rotate view |
| Space + Left mouse button | Grab |

Line colors:
* Green: Cursor is within range to interact
* Red: Cursor is out of range to interact
* Blue: Clicking
* Yellow: Grab mode enabled

Example of grabbing (notice the cursor turn yellow when Space is held down):

<section>
    <embed-video width="100%">
        <video-source handle="GIW1UgI1U-YAYLsBADNamx8rXsR7bosWAAAF" />
    </embed-video>
</section>

**Note**: The intersecting lines in your scene signify where clicks/grabs will actually be sent into the 3D scene. This may not line up perfectly with where your mouse cursor is on the Cast window.

## Troubleshooting

#### I've started input forwarding but I don't see the intersecting lines.

Please verify:
* You are on MQDH version 5.0
* You have followed all the steps to include input forwarding to your app, this must be added per-app. `CastInputForwardFeature` should be one of the features you return in `registerFeatures()`

Not seeing the intersecting lines means you are in general input forwarding mode, and not the Spatial SDK specific input forwarding mode. This is commonly fixed by restarting your app and selecting the input forward icon in your Cast window again. In rare cases you may need to restart your Cast window as well.

#### I'm getting errors related to libossdk

Make sure you have added the `<uses-native-library>` tag for libossdk, mentioned above in the "Adding input forwarding" section.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-tooling-dmi.md
---
title: Data Model Inspector
description: Learn how to use the Data Model Inspector feature to debug your Meta Spatial SDK project in real time.
last_updated: 2025-03-31
---

Manually debugging your Spatial SDK project can be difficult. The Data Model Inspector (DMI) tool makes debugging easier by providing a real-time view of your scene's data model in Android Studio. DMI lets you quickly identify issues by temporarily changing the attributes of entities without having to rebuild your app. If you'd rather make permanent changes without having to rebuild, use the [Hot Reload](/documentation/spatial-sdk/spatial-sdk-hot-reload/) feature.

Here's an example of using the DMI with input forwarding to grab a basketball. Note how whenever the user interacts with the basketball, the `isGrabbed` boolean updates in real time.

<section>
  <embed-video width="100%">
    <video-source handle="GDZqNxz8poTWz64FAGFZxU3kQeVjbosWAAAF" />
  </embed-video>
</section>

## Before you begin

* [Change your project's runtime to include JCEF](https://www.jetbrains.com/help/idea/switching-boot-jdk.html).
* (Optional, but highly recommended) Enable [Input Forwarding](/documentation/spatial-sdk/spatial-sdk-tooling-castinputforward).
* Install the [Meta Horizon Android Studio Plugin](/documentation/spatial-sdk/spatial-sdk-android-studio-plugin/).

## Manually add the Data Model Inspector

If you're using either a template created by the Meta Horizon Android Studio plugin, or any of the Spatial SDK samples, skip this section because the DMI is already included in your project. If you're not using a template or the samples, follow these steps to add the DMI to your project.

1. In the `dependencies` block of your project's `build.gradle.kts` file, add this line.

    ```kotlin
    implementation("com.meta.spatial:meta-spatial-sdk-datamodelinspector:$metaSpatialSdkVersion")
    ```

2. In the `imports` section of your main activity file, add this line.

    ```kotlin
    import com.meta.spatial.datamodelinspector.DataModelInspectorFeature
    ```

3. In the `RegisterFeatures()` method of your main activity, add this line.

    ```kotlin
    features.add(DataModelInspectorFeature(spatial, this.componentManager))
    ```

## Use the Data Model Inspector

Once you build and run your app, you access the DMI via a dedicated panel in Android Studio.

1. Connect your headset to your computer.

2. (Optional) If you set up input forwarding, in Meta Quest Developer Hub, start casting and enable input forwarding.

3. Build and run your app.

4. On the right toolbar of Android Studio, click the Meta logo to open the Meta Horizon Android Studio Plugin.

    The Data Model Inspector panel opens.

5. Ensure the port listed in the Data Model Inspector panel matches the one specified in your DataModelInspectorFeature registration. The DataModelInspectorFeature’s default port is 8011.

6. In the Data Model Inspector panel, click the refresh icon next to the port number to refresh the panel.

    The panel displays a list of entities in your scene.

7. Interact with entities in your scene to see the changes appear in the DMI.

## Common Tasks

### Selecting entities

* Select entities by either clicking on the entity header in the table or clicking on the entity in your 3D scene.

    This will highlight the header blue, and its child rows gray. This will also draw a red debug box around the entity in the 3D scene.


* To disable selecting entities by clicking them in the scene, click the lock icon (**Lock In-App Selection**) at the top of the Data Model Inspector panel.

### Searching and filtering

* Perform a fuzzy search on your attribute names, types, and values by typing them in the top search bar.
* Narrow your search by clicking the funnel icon and specifying which values you’d like to search by.
* Filter your view by clicking “Selected Only” in the filter dropdown.
* Filter your view by clicking “Recently Deleted” in the filter dropdown. The Deleted view does not support selection or edits.
* Clear all selected entities by clicking the broom icon.

### Editing attributes

Most attributes are editable. However, editing isn't supported for Map, Entity, and UUID.

1. Initiate an edit by clicking on an attribute in the table.

    This highlights the row and replaces the values with input forms to edit.

2. Change the values, and then click the check mark icon, or press the **Enter** key while the cursor is inside any of the input fields.

### Miscellaneous

* Expand all rows or collapse all rows by clicking their respective icons.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-tutorial-shared-content.md
---
title: Continue building your first Spatial SDK app
description: This tutorial continues the process of building a spatial application using Meta Spatial Editor and Meta Spatial SDK.
last_updated: 2024-04-22
---

In this tutorial, you'll continue building a Spatial SDK app with Spatial Editor by learning about common processes like importing assets and adding and creating components. By the end of this tutorial, you'll have a grabbable basketball in your scene that a robot will constantly look at.

## Import an asset

In the Spatial Editor, imported assets are stored in the asset panel. To learn more about importing assets, see [Import and manage assets](/documentation/spatial-sdk/spatial-editor-import-manage-assets).

1. If you haven't already opened the composition in Spatial Editor, complete [Open the composition in Spatial Editor](/documentation/spatial-sdk/create-new-spatial-sdk-app#optional-open-the-composition-in-spatial-editor).

2. Download this 3D model of a basketball hoop.

    <section>
    <file-link handle="GMtoNxw8pQ3kSygIAAz6uy9NfpxgbosWAAAe">
        ZIP of basketball hoop 3D model
    </file-link>
    </section>

3. Once the ZIP folder has downloaded, extract it.

4. Open the subfolder **basketballHoop**. In it, you'll see the file **basketballHoop.glb**.

5. In Spatial Editor, click **File** > **Import**, then navigate to **basketballHoop.glb**, and click **Open** to import the model into your project.

6. If you're creating a new Spatial SDK app, skip to the next section. If you're adding Spatial SDK to an existing app, follow the remaining steps to add some additional assets.

7. In the toolbar, click the books icon (the **Open Asset Library** button).

    The asset library window appears.

8. In the asset library window, double-click the **robot** and **basketBall** models to add them to your assets. You'll use them in the next section.

    Once the models finish downloading, they will appear in the **Project Assets** panel.

    ![Robot, basketball, and basketball hoop assets in the Assets panel](images/tutorial-assets.png)

    <em>The robot, basketball, and basketball hoop assets in the Assets panel.</em>

## Add and position objects in the Viewport

In the Spatial Editor, the [Viewport](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-viewport) is the main area where you interact with and build your spatial environment. To learn more about positioning objects, see [Position and size objects](/documentation/spatial-sdk/spatial-editor-objects#position-and-size-objects).

1. Drag and drop the **robot**, **basketBall**, and **basketballHoop** models from the **Assets** panel to the [Composition](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-composition-panel) panel.

    The models appear in the viewport at the world origin, which is 0 on the X, Y, and Z axes.

2. In the **Composition** panel, select **basketballHoop**.

3. In the **basketballHoop** properties panel on the right, update the **Transformation** values to match these.

    - Translation
        - X: -2
        - Y: 0.15
        - Z: 1
    - Rotation
        - Y: 45
    - Scale
        - X: 0.25
        - Y: 0.25
        - Z: 0.25

4. Position the **basketball** model using the following values.

    - Translation
        - Y: 0.25
        - Z: 0.9

5. Position the **robot** model using the following values.

    - Translation
        - X: 1
        - Y: 1
        - Z: 0.6

Here's what the scene looks like in Spatial Editor once you've positioned the models.

![Models in the scene](images/spatial-sdk-assets-in-the-scene.png)

## Assign components

[Components](/documentation/spatial-sdk/spatial-editor-components) are an essential part of the [Entity-Component-System (ECS)](/documentation/spatial-sdk/spatial-sdk-ecs) architecture used in Spatial SDK. Components are containers for app data that provide specific functionalities to scene objects. For example, a [grabbable](/reference/spatial-sdk/latest/root/com.meta.spatial.toolkit/grabbable/) component makes any object it's attached to grabbable with raycasting. Some components are provided by the SDK, but you can also write your own custom components.

To assign components to entities with the Spatial Editor, follow these steps.

1. In the [Composition panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-composition-panel), select **basketball**.
2. In the [Properties panel](/documentation/spatial-sdk/spatial-editor-navigation-ui#the-properties-panel), add the `Grabbable` component to the basketball by clicking the **+** next to **Meta Spatial SDK Components**, searching for _Grabbable_, and then clicking the search result.

    **Note**: If you add custom components to a project, like the LookAt component you create later in this tutorial, they won't appear in the search results until you click the [Reload](/documentation/spatial-sdk/spatial-editor-components#reload-components) button in the **Meta Spatial SDK Components** popup.

3. Save the project by clicking **File** > **Save**.

## Explore the main activity

In Android, the main activity file contains the core [activity lifecycle](https://developer.android.com/guide/components/activities/activity-lifecycle) of a Spatial SDK app. The activity lifecycle consists of several boilerplate functions you need for Spatial SDK apps.

Some boilerplate functions are provided by Android, and some are specific to Spatial SDK. Here's a partial list of functions you'll see in a main activity file.

- `registerFeatures()`: Registers the VR feature with the framework.
- `onCreate()`: Initializes the activity and sets up the scene.
- `onSceneReady()`: Prepares the scene for rendering.
- `createUI()`: Creates the UI panel scene object.
- `loadGLXF()`: Loads the GLXF file with the robot and ball models. Callback code is called once the scene is ready.

 The main activity file also sets up the app's environment, including lighting and a skybox, loads 3D models from the corresponding `.glxf` file, and handles registering new panels.

The main activity file is named either `ImmersiveActivity.kt` or `CustomComponentsSampleActivity.kt` depending on which option you chose in [Build your first Spatial SDK app](/documentation/spatial-sdk/spatial-editor-create-app-content#choose-a-start-option).

## Create a custom component

A component consists of two files, an XML file and a Kotlin file. The XML file lists the component's attributes, and the Kotlin file defines what happens during each tick for entities that your component is attached to. For more information about components, see [Writing a new component](/documentation/spatial-sdk/spatial-sdk-component).

The sample app already includes the required files for the `LookAt` component, which causes an object to continually track a target object. The component uses two files, `LookAtSystem.kt` and `LookAt.xml`.

### LookAtSystem.kt

`LookAtSystem.kt` updates the entity's position and rotation to achieve the desired behavior. It executes every frame and updates entities that the `LookAt` component is attached to.

If you're adding Spatial SDK to a 2D app, you'll need to uncomment this file.

1. Select the contents of `app/src/quest/java/com/meta/media/templateLookAtSystem.kt` and then uncomment them by clicking **Code** > **Comment with Block Comment** in the toolbar.
2. Save the file.

### LookAt.xml

`LookAt.xml` defines the reusable component with the following customizable attributes:

- `target`: The entity that this entity should look at.
- `lookAtHead`: A boolean value indicating whether the entity should look at the head of the target entity or its center.
- `axis`: An enumeration value indicating which axis the entity should look at. It can be set to ALL, Y, or other values.
- `speed`: A float value indicating how fast the entity should rotate to look at the target.
- `offset`: A Vector3 value indicating the offset from the target position that the entity should look at.

If you're adding Spatial SDK to a 2D app, you'll need to uncomment this file.

1. Select the contents of `app/src/main/components/LookAt.xml` and then uncomment them by clicking **Code** > **Comment with Block Comment** in the toolbar.
2. Save the file.

## Register component in the main activity

Now that your component is ready, you'll register it with both the component manager and the system manager so you can generate it as needed.

1. Open the main activity file for your app (the file is named either `ImmersiveActivity.kt` or `CustomComponentsSampleActivity.kt`).

2. Inside the `onCreate` function, underneath `// TODO: register the LookAt system and component`, add the following code to register the LookAt component and the LookAtSystem.

    ```kotlin
    componentManager.registerComponent<LookAt>(LookAt.Companion)
    systemManager.registerSystem(LookAtSystem())
    ```

3. If you get an `Unresolved reference` error, in the `imports` section at the top of the file, add these two dependencies.

    ```kotlin
    import com.meta.spatial.samples.customcomponentsstartersample.LookAt
    import com.meta.spatial.samples.customcomponentsstartersample.LookAtSystem
    ```

## Add custom component to an entity and preview it

You can add components to entities either via the Spatial Editor UI or programmatically.
Choose one of the following options:

- [Add component with Spatial Editor](#add-component-with-spatial-editor)
- [Add component programmatically](#add-component-programmatically)

### Add component with Spatial Editor

1. If you haven't reloaded your project in Spatial Editor since you added the `LookAt.xml` file, then [reload](/documentation/spatial-sdk/spatial-editor-components#reload-components) the **Meta Spatial SDK Components** list.
    ![Reload components in Editor](images/spatial-editor-reload-component.png)
2. In the **Composition** panel, select **robot**.
3. In the **robot** properties panel on the right, search for _LookAt_, and then select the **LookAt** search result from the list. Now the **LookAt** component is added to the robot.
4. In the **LookAt** component's properties, set the **target** entity to the **basketball** entity.
5. Change the second field of **offset** to _180_.

    ![Assign LookAt component to Robot in Editor](images/spatial-editor-assign-entity-custom-look-at-component.png)

### Add component programmatically

Underneath `// TODO add the LookAt component to the robot so it points at the basketBall`, add the following code.

```kotlin
val robot = composition.getNodeByName("robot").entity
val basketBall = composition.getNodeByName("basketBall").entity
robot.setComponent(LookAt(basketBall, offset = Vector3(x = 0f, y = 180f, z = 0f)))
```

Here's what the code does:

- Creates variables for the robot and basketball using the `getNodeByName` function on the composition.
- Uses the `setComponent` function on the robot entity to add the `LookAt` component and set the basketball as the target entity.
- Adds an offset to ensure the robot points correctly at the basketball.

### Preview the component

1. In Android Studio, click the green **Run 'app'** button.

2. Move the ball by hovering over it with your controller, pressing the trigger, and then moving your hand.

    As you grab and move the ball, the LookAt component rotates the robot to face the ball.

    <section>
    <embed-video width="100%">
    <video-source handle="GDNrNxyQ5MsBfdcGAO7fKQxTq2lObosWAAAF" />
    </embed-video>
    </section>

## (Optional) Create, modify, and register a panel

This section briefly explains how to add a new panel to your scene via Spatial Editor and customize the panel's content. For a detailed explanation of this process, see [Register 2D panels](/documentation/spatial-sdk/spatial-sdk-2dpanel-registration).

1. Open the app's `Main.metaspatial` file in Meta Spatial Editor.

2. In the upper left toolbar next to the cylinder button, click the **Add 2D Panel** button.

    ![Add a panel in Spatial Editor](/images/spatial-editor-add-panel-button.png)

      A panel appears at the world origin of the scene.

3. In the **Properties** panel, set **ID** to the following:

    ```xml
    @layout/ui_example2
    ```

    The ID is a file path consisting of two parts. The _@layout/_ prefix points to the **layout** folder in the sample's Android Studio project. _ui_example2_ refers to the file `ui_example2.xml`, which you'll create in the next section. That file will add content to the panel.

4. Set the panel's **Translation** values as follows.
    - X: 2
    - Y: 0.8
    - Z: 1.75

5. In the **Composition** panel, right-click on **Panel1**, select **Rename...**, and enter _Panel 2_.

6. In the top toolbar, select **File** > **Save**.

7. Open Android Studio.

8. In the file directory panel, find the file `app/src/main/res/layout/ui_example.xml`.

9. Duplicate the `ui_example.xml` file and name the copy **ui_example2.xml**.

10. In `app/src/main/res/values/ids.xml`, inside the `<resources>` block,  add a line for the new panel.

    ```XML
    <item type="id" name="ui_example2" />
    ```

11. In your main activity file, below the comment `TODO: add a second panel` in the `registerPanels()` method, add this code to register your new panel.

    ```kotlin
    PanelRegistration(R.layout.ui_example2) { entity ->
        config {
            themeResourceId = R.style.PanelAppThemeTransparent
            includeGlass = false
            enableTransparent = true
        }
    }
    ```

12. Save the file.

13. Deploy your app to the headset by clicking the **Run 'app'** button in Android Studio.

    The second panel will appear in your scene behind the robot.

    ![Second panel behind the robot](images/spatial-sdk-second-panel.jpg)

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/spatial-sdk-writing-new-system.md
---
title: Write a new system
description: Writing a new system with Meta Spatial SDK.
last_updated: 2024-10-16
---

## Overview

The core of Spatial SDK's computation is its components. Systems function every tick, typically involving one or more entity queries and modifications to component data.

## Steps

To construct a new system, follow these steps:

1. Begin by defining your class. Spatial SDK Systems utilize `com.meta.spatial.core.System`. The header should be as follows:

    ```kotlin
    class UpAndDownSystem() : SystemBase() {
    ```

2. Override the execute function. This function operates every tick, and you’ll use it for the operations you wish to perform:

    ```kotlin
    override fun execute() {
    ```

   The following steps outline an example where specific entities are queried and caused to move upward until a certain point, at which they return to their initial location in a continuous loop.

3. Create a query to pull data from the data model. The following query examines all entities with an `UpAndDown` component and a `Transform`:

    ```kotlin
    val q = Query.where { has(UpAndDown.id, Transform.id) }
    for (entity in q.eval()) {
    ```

4. Run an operation on the entity to change the data and establish the new component:

    ```kotlin
    for (entity in q.eval()) { // the line from earlier
      val transform = entity.getComponent<Transform>()
      transform.transform.t.y += (0.2f)
      transform.transform.t.y %= 1
      entity.setComponent(transform)
    }
    ```

5. The entire system construction process is combined as follows:

    ```kotlin
    //UpAndDownSystem.kt
    class UpAndDownSystem() : SystemBase() {
      override fun execute() {
        val q = Query.where { has(UpAndDown.id, Transform.id) }
        for (entity in q.eval()) {
          val transform = entity.getComponent<Transform>()
          transform.transform.t.y += (0.2f)
          transform.transform.t.y %= 1
          entity.setComponent(transform)
        }
      }
    }
    ```

6. Register your system.

    ```kotlin
    //MyActivity.kt
    systemManager.registerSystem(UpAndDownSystem())
    ```

7. Your code will run the execute function every tick.

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-adb.md
---
title: Android Debug Bridge (ADB) for Meta Quest
engine: spatial-sdk
shell: tools
last_updated: 2025-01-07
---

{%include tools-shared/ts-adb.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-gpumeminfo.md
---
title: Track GPU memory usage with gpumeminfo
engine: spatial-sdk
shell: tools
last_updated: 2025-01-07
---

{%include tools-shared/ts-gpumeminfo.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-logcat-stats.md
---
title: Logcat stats definitions
engine: spatial-sdk
shell: tools
last_updated: 2025-01-07
---

{%include tools-shared/ts-logcat-stats.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-logcat.md
---
title: Collect logs with Logcat
engine: spatial-sdk
shell: tools
last_updated: 2025-01-07
---

{%include tools-shared/ts-logcat.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-basic-usage.md
---
title: Manage your Headset with MQDH
engine: spatial-sdk
last_updated: 2024-12-06
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-basic-usage.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-compositor-layer.md
---
title: Layer Visibility Control in VR Compositor
description: Describes how to use Meta Quest Developer Hub to control compositor layer visibility for performance analysis.
engine: spatial-sdk
last_updated: 2024-12-06
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-compositor-layer.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-custom-commands.md
---
title: Create a Custom Command
engine: spatial-sdk
last_updated: 2024-12-06
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-custom-commands.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-deploy-build.md
---
title: Deploy Build on Headset
engine: spatial-sdk
last_updated: 2024-12-06
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-deploy-build.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-device-setup.md
---
title: Set Up Headset with MQDH
engine: spatial-sdk
last_updated: 2024-12-06
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-device-setup.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-download-tools.md
---
title: MQDH Downloads
engine: spatial-sdk
last_updated: 2024-12-06
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-download-tools.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-file-manager.md
---
title: Explore File Manager
engine: spatial-sdk
last_updated: 2024-12-06
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-file-manager.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-getting-started.md
---
title: Get Started with Meta Quest Developer Hub
engine: spatial-sdk
last_updated: 2024-12-06
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-getting-started.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-logs-metrics.md
---
title: Performance Analyzer and Metrics
engine: spatial-sdk
last_updated: 2024-12-06
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-logs-metrics.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-media.md
---
title: Debugging Tools
engine: spatial-sdk
last_updated: 2025-02-26
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-media.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-multiuser.md
---
title: Add, Remove, and Switch Between Multi-User Accounts
engine: spatial-sdk
last_updated: 2024-12-06
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-multiuser.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-report-a-bug.md
---
title: Submit and Track Bugs and Feature Requests
engine: spatial-sdk
last_updated: 2024-12-12
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-report-a-bug.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh-troubleshooting.md
---
title: Troubleshooting MQDH
engine: spatial-sdk
last_updated: 2024-12-06
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh-troubleshooting.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-mqdh.md
---
title: Meta Quest Developer Hub
description: Overview of the Platform SDK Security features
engine: spatial-sdk
last_updated: 2024-12-06
related_docs:
 - title: Download MQDH for Windows
   path: /downloads/package/oculus-developer-hub-win
 - title: Download MQDH for Mac
   path: /downloads/package/oculus-developer-hub-mac
---

{%include tools-shared/ts-mqdh.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-ovrgpuprofiler.md
---
title: Use ovrgpuprofiler for GPU profiling
engine: spatial-sdk
shell: tools
last_updated: 2025-01-07
---

{%include tools-shared/ts-ovrgpuprofiler.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-perfettoguide.md
---
title: How to Take Perfetto Traces with Meta Quest Developer Hub
description: Describes how to use Meta Quest Developer Hub to take a Perfetto trace and use it for performance analysis during Meta Quest development.
engine: spatial-sdk
last_updated: 2024-12-06
---

{%include tools-shared/ts-perfettoguide.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-simpleperf.md
---
title: Use Simpleperf for CPU profiling
description: Describes how to use the Android tool Simpleperf for CPU profiling during Meta Quest development.
engine: spatial-sdk
shell: tools
last_updated: 2025-01-07
---

{%include tools-shared/ts-simpleperf.md %}

# arvr/projects/public-developer-docs/mdsourcedc/documentation/spatial-sdk/ts-systemproperties.md
---
title: Configure Android system properties on Meta Quest
engine: spatial-sdk
shell: tools
last_updated: 2025-01-07
---

{%include tools-shared/ts-systemproperties.md %}

